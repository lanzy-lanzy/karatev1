#!/usr/bin/env python
"""
Diagnostic script to identify why auto-matching is finding no valid pairings.
"""
import os
import sys
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'karate.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from core.models import Trainee, Event, EventRegistration, Match
from core.services.matchmaking import MatchmakingService, are_belts_adjacent

def diagnose_event(event_id=None, event_name=None):
    """Diagnose why an event has no valid matches."""
    
    # Get the event
    if event_id:
        event = Event.objects.get(id=event_id)
    elif event_name:
        event = Event.objects.get(name__icontains=event_name)
    else:
        # Get first event with registrations
        events = Event.objects.filter(registrations__status='registered').distinct()
        if events.count() == 0:
            print("No events with registrations found.")
            return
        event = events.first()
    
    print("\n" + "=" * 100)
    print(f"DIAGNOSING EVENT: {event.name}")
    print("=" * 100)
    
    # Get registered trainees
    registrations = EventRegistration.objects.filter(
        event=event,
        status='registered'
    ).select_related('trainee__profile')
    
    trainees = [reg.trainee for reg in registrations]
    
    print(f"\nRegistered Trainees: {len(trainees)}")
    print("-" * 100)
    print(f"{'Name':<30} {'Belt':<12} {'Weight':<10} {'Class':<18} {'Age':<8} {'DOB':<12}")
    print("-" * 100)
    
    for trainee in trainees:
        name = trainee.profile.user.get_full_name() or trainee.profile.user.username
        belt = trainee.belt_rank
        weight = float(trainee.weight)
        wclass = trainee.weight_class or "NOT SET"
        age = trainee.age or "N/A"
        dob = trainee.profile.date_of_birth or "Not Set"
        
        print(f"{name:<30} {belt:<12} {weight:<10.2f} {wclass:<18} {str(age):<8} {str(dob):<12}")
    
    # Analyze constraints
    print("\n" + "=" * 100)
    print("CONSTRAINT ANALYSIS")
    print("=" * 100)
    
    service = MatchmakingService()
    
    # Check all pairings
    total_pairs = 0
    weight_valid = 0
    belt_valid = 0
    age_valid = 0
    all_valid = 0
    
    invalid_reasons = {
        'weight': [],
        'belt': [],
        'age': [],
        'weight_belt': [],
        'weight_age': [],
        'belt_age': [],
        'all_three': []
    }
    
    for i, t1 in enumerate(trainees):
        for t2 in trainees[i+1:]:
            total_pairs += 1
            
            # Check constraints
            weight_diff = abs(t1.weight - t2.weight)
            weight_ok = weight_diff <= Decimal('5.0')
            
            belt_ok = are_belts_adjacent(t1.belt_rank, t2.belt_rank)
            
            age1 = t1.age or 0
            age2 = t2.age or 0
            age_diff = abs(age1 - age2)
            age_ok = age_diff <= 3 or (t1.age is None or t2.age is None)
            
            # Count valid constraints
            if weight_ok:
                weight_valid += 1
            if belt_ok:
                belt_valid += 1
            if age_ok:
                age_valid += 1
            
            # Check what failed
            if weight_ok and belt_ok and age_ok:
                all_valid += 1
            else:
                # Categorize failure
                name1 = t1.profile.user.get_full_name() or t1.profile.user.username
                name2 = t2.profile.user.get_full_name() or t2.profile.user.username
                pair_str = f"{name1} vs {name2}"
                
                if not weight_ok and not belt_ok and not age_ok:
                    invalid_reasons['all_three'].append(pair_str)
                elif not weight_ok and not belt_ok:
                    invalid_reasons['weight_belt'].append(pair_str)
                elif not weight_ok and not age_ok:
                    invalid_reasons['weight_age'].append(pair_str)
                elif not belt_ok and not age_ok:
                    invalid_reasons['belt_age'].append(pair_str)
                elif not weight_ok:
                    invalid_reasons['weight'].append((pair_str, f"Δ{weight_diff:.1f}kg"))
                elif not belt_ok:
                    invalid_reasons['belt'].append(pair_str)
                elif not age_ok:
                    invalid_reasons['age'].append((pair_str, f"Δ{age_diff}yr"))
    
    print(f"\nTotal possible pairings: {total_pairs}")
    print(f"  Weight constraint (≤5kg):     {weight_valid:3}/{total_pairs} ({100*weight_valid/total_pairs:5.1f}%)")
    print(f"  Belt constraint (adjacent):   {belt_valid:3}/{total_pairs} ({100*belt_valid/total_pairs:5.1f}%)")
    print(f"  Age constraint (≤3yr):        {age_valid:3}/{total_pairs} ({100*age_valid/total_pairs:5.1f}%)")
    print(f"  ALL constraints met:          {all_valid:3}/{total_pairs} ({100*all_valid/total_pairs:5.1f}%) ← VALID MATCHES")
    
    # Show why pairings are failing
    print("\n" + "=" * 100)
    print("WHY PAIRINGS ARE FAILING")
    print("=" * 100)
    
    if invalid_reasons['all_three']:
        print(f"\nFail ALL three constraints ({len(invalid_reasons['all_three'])} pairs):")
        for pair in invalid_reasons['all_three'][:5]:
            print(f"  • {pair}")
        if len(invalid_reasons['all_three']) > 5:
            print(f"  ... and {len(invalid_reasons['all_three']) - 5} more")
    
    if invalid_reasons['weight_belt']:
        print(f"\nFail Weight AND Belt ({len(invalid_reasons['weight_belt'])} pairs):")
        for pair in invalid_reasons['weight_belt'][:5]:
            print(f"  • {pair}")
        if len(invalid_reasons['weight_belt']) > 5:
            print(f"  ... and {len(invalid_reasons['weight_belt']) - 5} more")
    
    if invalid_reasons['weight_age']:
        print(f"\nFail Weight AND Age ({len(invalid_reasons['weight_age'])} pairs):")
        for pair in invalid_reasons['weight_age'][:5]:
            print(f"  • {pair}")
        if len(invalid_reasons['weight_age']) > 5:
            print(f"  ... and {len(invalid_reasons['weight_age']) - 5} more")
    
    if invalid_reasons['weight']:
        print(f"\nFail Weight only ({len(invalid_reasons['weight'])} pairs):")
        for pair, info in invalid_reasons['weight'][:5]:
            print(f"  • {pair} ({info})")
        if len(invalid_reasons['weight']) > 5:
            print(f"  ... and {len(invalid_reasons['weight']) - 5} more")
    
    if invalid_reasons['belt']:
        print(f"\nFail Belt only ({len(invalid_reasons['belt'])} pairs):")
        for pair in invalid_reasons['belt'][:5]:
            print(f"  • {pair}")
        if len(invalid_reasons['belt']) > 5:
            print(f"  ... and {len(invalid_reasons['belt']) - 5} more")
    
    if invalid_reasons['age']:
        print(f"\nFail Age only ({len(invalid_reasons['age'])} pairs):")
        for pair, info in invalid_reasons['age'][:5]:
            print(f"  • {pair} ({info})")
        if len(invalid_reasons['age']) > 5:
            print(f"  ... and {len(invalid_reasons['age']) - 5} more")
    
    # Summary stats
    print("\n" + "=" * 100)
    print("RECOMMENDATIONS")
    print("=" * 100)
    
    if all_valid == 0:
        print("\n⚠ NO VALID MATCHES FOUND")
        
        if weight_valid < total_pairs * 0.5:
            print("\n1. WEIGHT DISTRIBUTION IS TOO SPREAD OUT")
            print("   Solution: Register trainees with similar weights (within 5kg)")
            
            # Show weight range
            weights = [float(t.weight) for t in trainees]
            print(f"   Current weight range: {min(weights):.1f}kg - {max(weights):.1f}kg (span: {max(weights)-min(weights):.1f}kg)")
            print(f"   Recommendation: Keep within 10-15kg span for good pairings")
        
        if belt_valid < total_pairs * 0.5:
            print("\n2. BELT RANKS ARE TOO SPREAD OUT")
            print("   Solution: Register trainees of same/adjacent belt levels")
            
            # Show belt distribution
            belts = [t.belt_rank for t in trainees]
            from collections import Counter
            belt_counts = Counter(belts)
            print(f"   Current belt distribution:")
            for belt, count in sorted(belt_counts.items()):
                print(f"     - {belt}: {count} trainees")
            print(f"   Recommendation: Register multiple trainees from same/adjacent belts")
        
        if age_valid < total_pairs * 0.5:
            print("\n3. AGES ARE TOO SPREAD OUT")
            print("   Solution: Register trainees of similar ages (within 3 years)")
            print("   Note: This is optional - missing DOB is handled gracefully")
    
    else:
        print(f"\n✅ Found {all_valid} valid pairings!")
        print(f"   Matching is possible with current trainee data.")
        
        # Try to generate matches
        try:
            proposed = service.auto_match(event.id)
            print(f"\n   Auto-matching generated: {len(proposed)} matches")
            for i, match in enumerate(proposed, 1):
                print(f"     {i}. {match.competitor1.profile.user.get_full_name()} vs {match.competitor2.profile.user.get_full_name()} (score: {match.score:.2f})")
        except Exception as e:
            print(f"   Error during auto-matching: {e}")
    
    print("\n" + "=" * 100 + "\n")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Diagnose auto-matching issues')
    parser.add_argument('--event-id', type=int, help='Event ID to diagnose')
    parser.add_argument('--event-name', type=str, help='Event name substring to find')
    parser.add_argument('--all', action='store_true', help='Diagnose all events')
    
    args = parser.parse_args()
    
    if args.all:
        events = Event.objects.filter(registrations__status='registered').distinct()
        for event in events:
            diagnose_event(event_id=event.id)
    elif args.event_id:
        diagnose_event(event_id=args.event_id)
    elif args.event_name:
        diagnose_event(event_name=args.event_name)
    else:
        diagnose_event()

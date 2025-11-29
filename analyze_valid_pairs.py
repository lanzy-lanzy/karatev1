#!/usr/bin/env python
"""
Analyze which specific pairs are valid and trace the greedy matching algorithm.
"""
import os
import sys
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'karate.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from core.models import Trainee, Event, EventRegistration
from core.services.matchmaking import MatchmakingService, are_belts_adjacent, get_belt_index

def analyze_valid_pairs(event_id=None):
    """Show all valid pairs and trace the matching algorithm."""
    
    # Get event
    if event_id:
        event = Event.objects.get(id=event_id)
    else:
        events = Event.objects.filter(registrations__status='registered').distinct()
        if events.count() == 0:
            print("No events with registrations found.")
            return
        event = events.first()
    
    print("\n" + "=" * 120)
    print(f"ANALYZING VALID PAIRS FOR: {event.name}")
    print("=" * 120)
    
    # Get registered trainees
    registrations = EventRegistration.objects.filter(
        event=event,
        status='registered'
    ).select_related('trainee__profile')
    
    trainees = [reg.trainee for reg in registrations]
    service = MatchmakingService()
    
    # Find all valid pairs
    valid_pairs = []
    
    for i, t1 in enumerate(trainees):
        for t2 in trainees[i+1:]:
            if service._is_valid_pairing(t1, t2):
                weight_diff = abs(t1.weight - t2.weight)
                belt_diff = abs(get_belt_index(t1.belt_rank) - get_belt_index(t2.belt_rank))
                age_diff = abs((t1.age or 0) - (t2.age or 0))
                score = service._calculate_pairing_score(t1, t2)
                
                valid_pairs.append({
                    'trainee1': t1,
                    'trainee2': t2,
                    'weight_diff': float(weight_diff),
                    'belt_diff': belt_diff,
                    'age_diff': age_diff,
                    'score': score,
                    'idx1': i,
                    'idx2': trainees.index(t2)
                })
    
    print(f"\nTotal VALID pairs: {len(valid_pairs)}\n")
    
    # Sort by score
    valid_pairs.sort(key=lambda x: x['score'])
    
    # Show all valid pairs
    print("VALID PAIRS (sorted by score - lower is better):")
    print("-" * 120)
    print(f"{'#':<3} {'Score':<8} {'Trainee 1':<20} {'Trainee 2':<20} {'Weight':<12} {'Belt':<8} {'Age':<8}")
    print("-" * 120)
    
    for i, pair in enumerate(valid_pairs, 1):
        t1 = pair['trainee1']
        t2 = pair['trainee2']
        t1_name = t1.profile.user.get_full_name() or t1.profile.user.username
        t2_name = t2.profile.user.get_full_name() or t2.profile.user.username
        weight = f"Δ{pair['weight_diff']:.1f}kg"
        belt = f"Δ{pair['belt_diff']}"
        age = f"Δ{pair['age_diff']}yr"
        
        print(f"{i:<3} {pair['score']:<8.2f} {t1_name:<20} {t2_name:<20} {weight:<12} {belt:<8} {age:<8}")
    
    # Trace greedy algorithm
    print("\n" + "=" * 120)
    print("GREEDY MATCHING ALGORITHM TRACE")
    print("=" * 120)
    print("\nAlgorithm: Select best scoring pairs first, mark trainees as used, repeat\n")
    
    used_trainees = set()
    matches = []
    
    for idx, pair in enumerate(valid_pairs, 1):
        t1_idx = pair['idx1']
        t2_idx = pair['idx2']
        t1 = pair['trainee1']
        t2 = pair['trainee2']
        t1_name = t1.profile.user.get_full_name() or t1.profile.user.username
        t2_name = t2.profile.user.get_full_name() or t2.profile.user.username
        
        status = ""
        if t1_idx in used_trainees:
            status = f"❌ {t1_name} ALREADY USED"
        elif t2_idx in used_trainees:
            status = f"❌ {t2_name} ALREADY USED"
        else:
            status = f"✅ MATCHED"
            matches.append(pair)
            used_trainees.add(t1_idx)
            used_trainees.add(t2_idx)
        
        print(f"Step {idx}: {t1_name:20} vs {t2_name:20} (score: {pair['score']:.2f}) → {status}")
    
    print("\n" + "=" * 120)
    print("RESULT")
    print("=" * 120)
    print(f"\nMatches created: {len(matches)}")
    print(f"Trainees used: {len(used_trainees)}/{len(trainees)}")
    print(f"Trainees unmatched: {len(trainees) - len(used_trainees)}")
    
    if matches:
        print("\nMatches:")
        for i, match in enumerate(matches, 1):
            t1 = match['trainee1']
            t2 = match['trainee2']
            t1_name = t1.profile.user.get_full_name() or t1.profile.user.username
            t2_name = t2.profile.user.get_full_name() or t2.profile.user.username
            print(f"  {i}. {t1_name} vs {t2_name}")
    
    # Show unmatched
    unmatched = [t for i, t in enumerate(trainees) if i not in used_trainees]
    if unmatched:
        print("\nUnmatched trainees:")
        for t in unmatched:
            name = t.profile.user.get_full_name() or t.profile.user.username
            print(f"  • {name} ({t.belt_rank}, {t.weight}kg)")
    
    # Analysis
    print("\n" + "=" * 120)
    print("ANALYSIS")
    print("=" * 120)
    
    if len(valid_pairs) == 0:
        print("\nNo valid pairs exist. Issue with constraints.")
    elif len(matches) == 0:
        print("\n⚠ PROBLEM: Valid pairs exist but greedy algorithm can't create matches!")
        print("\nLikely cause:")
        print("  The 7 valid pairs are 'isolated' - they don't form a connected matching.")
        print("  Example: If only pair is (A-B), both A and B get used, leaving others unmatched.")
        print("\nExample configuration that causes this:")
        print("  Valid pairs: A-B, C-D, E-F, G-H")
        print("  Greedy picks: A-B (both used)")
        print("           then: C-D (both used)")  
        print("           then: E-F (both used)")
        print("           then: G-H (both used)")
        print("  Result: All isolated pairs, might work if even number of trainees")
        print("\n  OR:")
        print("  Valid pairs: A-B, A-C, B-C (only 3 trainees)")
        print("  Greedy picks: A-B (both used)")
        print("           then: No more pairs available (A and B already used)")
        print("  Result: 1 match, 1 unmatched (C)")
    elif len(matches) < len(valid_pairs) / 2:
        print(f"\n⚠ WARNING: Only {len(matches)} matches created from {len(valid_pairs)} valid pairs!")
        print("This is normal if valid pairs form scattered groups.")
    else:
        print(f"\n✅ Successfully created {len(matches)} matches from {len(valid_pairs)} valid pairs.")
    
    print("\n" + "=" * 120 + "\n")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze valid pairs in event')
    parser.add_argument('--event-id', type=int, help='Event ID')
    
    args = parser.parse_args()
    
    analyze_valid_pairs(event_id=args.event_id)

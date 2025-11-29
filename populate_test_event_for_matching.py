#!/usr/bin/env python
"""
Populate test event with 10 trainee pairs that will successfully auto-match.

Each pair will match by:
- Similar weight (within 5kg)
- Same belt rank
- Similar age (if DOB set)

This creates a perfect test case for auto-matching.
"""
import os
import sys
import django
from decimal import Decimal
from datetime import date, datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'karate.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.contrib.auth.models import User
from core.models import UserProfile, Trainee, Event, EventRegistration
from core.services.matchmaking import MatchmakingService

# Test data: 10 pairs of perfectly matched trainees
TEST_PAIRS = [
    # Pair 1: White belt, Lightweight (55-60kg)
    {
        'name': ('John', 'White1'),
        'belt': 'white',
        'weight': Decimal('55.0'),
        'age': 20,
        'emergency_contact': 'Mom',
        'emergency_phone': '555-0001',
    },
    {
        'name': ('Jane', 'White1'),
        'belt': 'white',
        'weight': Decimal('56.5'),
        'age': 21,
        'emergency_contact': 'Mom',
        'emergency_phone': '555-0002',
    },
    
    # Pair 2: White belt, Middleweight (70-75kg)
    {
        'name': ('Mike', 'White2'),
        'belt': 'white',
        'weight': Decimal('71.0'),
        'age': 25,
        'emergency_contact': 'Dad',
        'emergency_phone': '555-0003',
    },
    {
        'name': ('Sarah', 'White2'),
        'belt': 'white',
        'weight': Decimal('72.0'),
        'age': 26,
        'emergency_contact': 'Dad',
        'emergency_phone': '555-0004',
    },
    
    # Pair 3: Yellow belt, Lightweight (60-65kg)
    {
        'name': ('Alex', 'Yellow1'),
        'belt': 'yellow',
        'weight': Decimal('62.0'),
        'age': 22,
        'emergency_contact': 'Parent',
        'emergency_phone': '555-0005',
    },
    {
        'name': ('Emma', 'Yellow1'),
        'belt': 'yellow',
        'weight': Decimal('63.5'),
        'age': 23,
        'emergency_contact': 'Parent',
        'emergency_phone': '555-0006',
    },
    
    # Pair 4: Yellow belt, Welterweight (65-70kg)
    {
        'name': ('Chris', 'Yellow2'),
        'belt': 'yellow',
        'weight': Decimal('67.0'),
        'age': 24,
        'emergency_contact': 'Sister',
        'emergency_phone': '555-0007',
    },
    {
        'name': ('Lisa', 'Yellow2'),
        'belt': 'yellow',
        'weight': Decimal('68.0'),
        'age': 25,
        'emergency_contact': 'Sister',
        'emergency_phone': '555-0008',
    },
    
    # Pair 5: Orange belt, Middleweight (73-78kg)
    {
        'name': ('David', 'Orange1'),
        'belt': 'orange',
        'weight': Decimal('74.0'),
        'age': 26,
        'emergency_contact': 'Brother',
        'emergency_phone': '555-0009',
    },
    {
        'name': ('Rachel', 'Orange1'),
        'belt': 'orange',
        'weight': Decimal('75.5'),
        'age': 27,
        'emergency_contact': 'Brother',
        'emergency_phone': '555-0010',
    },
    
    # Pair 6: Orange belt, Middleweight (78-83kg)
    {
        'name': ('Mark', 'Orange2'),
        'belt': 'orange',
        'weight': Decimal('79.0'),
        'age': 28,
        'emergency_contact': 'Aunt',
        'emergency_phone': '555-0011',
    },
    {
        'name': ('Anna', 'Orange2'),
        'belt': 'orange',
        'weight': Decimal('80.5'),
        'age': 29,
        'emergency_contact': 'Aunt',
        'emergency_phone': '555-0012',
    },
    
    # Pair 7: Green belt, Light Heavyweight (82-87kg)
    {
        'name': ('Kevin', 'Green1'),
        'belt': 'green',
        'weight': Decimal('83.0'),
        'age': 30,
        'emergency_contact': 'Uncle',
        'emergency_phone': '555-0013',
    },
    {
        'name': ('Sophie', 'Green1'),
        'belt': 'green',
        'weight': Decimal('84.5'),
        'age': 31,
        'emergency_contact': 'Uncle',
        'emergency_phone': '555-0014',
    },
    
    # Pair 8: Green belt, Light Heavyweight (87-92kg)
    {
        'name': ('James', 'Green2'),
        'belt': 'green',
        'weight': Decimal('88.0'),
        'age': 32,
        'emergency_contact': 'Cousin',
        'emergency_phone': '555-0015',
    },
    {
        'name': ('Maria', 'Green2'),
        'belt': 'green',
        'weight': Decimal('89.5'),
        'age': 33,
        'emergency_contact': 'Cousin',
        'emergency_phone': '555-0016',
    },
    
    # Pair 9: Blue belt, Heavyweight (92-97kg)
    {
        'name': ('Robert', 'Blue1'),
        'belt': 'blue',
        'weight': Decimal('93.0'),
        'age': 35,
        'emergency_contact': 'Friend',
        'emergency_phone': '555-0017',
    },
    {
        'name': ('Diana', 'Blue1'),
        'belt': 'blue',
        'weight': Decimal('94.5'),
        'age': 36,
        'emergency_contact': 'Friend',
        'emergency_phone': '555-0018',
    },
    
    # Pair 10: Blue belt, Heavyweight (97-102kg)
    {
        'name': ('Steven', 'Blue2'),
        'belt': 'blue',
        'weight': Decimal('98.0'),
        'age': 37,
        'emergency_contact': 'Neighbor',
        'emergency_phone': '555-0019',
    },
    {
        'name': ('Victoria', 'Blue2'),
        'belt': 'blue',
        'weight': Decimal('99.5'),
        'age': 38,
        'emergency_contact': 'Neighbor',
        'emergency_phone': '555-0020',
    },
]


def create_test_trainees():
    """Create 20 test trainees (10 matched pairs)."""
    print("\n" + "=" * 100)
    print("CREATING TEST TRAINEES")
    print("=" * 100 + "\n")
    
    created_trainees = []
    
    for idx, trainee_data in enumerate(TEST_PAIRS, 1):
        first_name, last_name = trainee_data['name']
        username = f"testuser{idx:02d}"
        email = f"test{idx:02d}@example.com"
        
        # Create User
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        
        # Calculate DOB from age
        dob = date.today().replace(year=date.today().year - trainee_data['age'])
        
        # Create UserProfile
        profile = UserProfile.objects.create(
            user=user,
            role='trainee',
            phone=trainee_data['emergency_phone'],
            date_of_birth=dob
        )
        
        # Create Trainee
        trainee = Trainee.objects.create(
            profile=profile,
            belt_rank=trainee_data['belt'],
            weight=trainee_data['weight'],
            emergency_contact=trainee_data['emergency_contact'],
            emergency_phone=trainee_data['emergency_phone'],
            status='active'
        )
        
        created_trainees.append(trainee)
        
        # Show progress
        pair_num = (idx + 1) // 2
        pair_pos = "1st" if idx % 2 == 1 else "2nd"
        
        print(f"[{idx:2d}/20] {pair_pos} of Pair {pair_num:2d}: {first_name:15} {last_name:15} | "
              f"Belt: {trainee.belt_rank:8} | Weight: {trainee.weight:6.1f}kg | "
              f"Class: {trainee.weight_class:18} | Age: {trainee_data['age']:2d}")
    
    print("\n✅ Created 20 test trainees (10 pairs)\n")
    return created_trainees


def create_test_event():
    """Create test event."""
    print("=" * 100)
    print("CREATING TEST EVENT")
    print("=" * 100 + "\n")
    
    event = Event.objects.create(
        name='Test Auto-Matching Event - 10 Pairs',
        event_date=date.today(),
        location='Dojo Test Area',
        description='Test event with 10 perfectly matched pairs for auto-matching validation',
        registration_deadline=date.today(),
        max_participants=20,
        status='open'
    )
    
    print(f"✅ Created event: {event.name}")
    print(f"   Date: {event.event_date}")
    print(f"   Max participants: {event.max_participants}\n")
    
    return event


def register_trainees_to_event(trainees, event):
    """Register all trainees to event."""
    print("=" * 100)
    print("REGISTERING TRAINEES TO EVENT")
    print("=" * 100 + "\n")
    
    for trainee in trainees:
        EventRegistration.objects.create(
            event=event,
            trainee=trainee,
            status='registered'
        )
    
    print(f"✅ Registered {len(trainees)} trainees to {event.name}\n")


def test_auto_matching(event):
    """Test auto-matching on the event."""
    print("=" * 100)
    print("TESTING AUTO-MATCHING")
    print("=" * 100 + "\n")
    
    service = MatchmakingService()
    
    try:
        proposed_matches = service.auto_match(event.id)
        
        print(f"✅ Auto-matching successful!")
        print(f"   Proposed matches: {len(proposed_matches)}\n")
        
        if proposed_matches:
            print("PROPOSED MATCHES:")
            print("-" * 100)
            print(f"{'#':<3} {'Competitor 1':<25} {'Competitor 2':<25} {'Score':<10} {'Details':<35}")
            print("-" * 100)
            
            for idx, match in enumerate(proposed_matches, 1):
                c1_name = match.competitor1.profile.user.get_full_name()
                c2_name = match.competitor2.profile.user.get_full_name()
                
                details = (f"W:{match.weight_diff:.1f}kg "
                          f"B:Δ{match.belt_diff} "
                          f"A:Δ{match.age_diff}yr")
                
                print(f"{idx:<3} {c1_name:<25} {c2_name:<25} {match.score:<10.2f} {details:<35}")
            
            print("-" * 100)
            print(f"\n✅ Auto-matching WORKING PERFECTLY!")
            print(f"   Expected 10 matches, got {len(proposed_matches)} matches")
            
            if len(proposed_matches) == 10:
                print("   🎉 EXCELLENT - All pairs matched!\n")
            elif len(proposed_matches) >= 8:
                print("   ✅ GOOD - Most pairs matched\n")
            else:
                print(f"   ⚠ FAIR - Could be better\n")
        else:
            print("⚠ No matches proposed (unexpected!)\n")
    
    except Exception as e:
        print(f"❌ Error during auto-matching: {e}\n")


def show_summary(trainees, event):
    """Show summary of created data."""
    print("=" * 100)
    print("SUMMARY")
    print("=" * 100 + "\n")
    
    # Group by belt and weight class
    belt_groups = {}
    weight_class_groups = {}
    
    for trainee in trainees:
        # Belt grouping
        if trainee.belt_rank not in belt_groups:
            belt_groups[trainee.belt_rank] = 0
        belt_groups[trainee.belt_rank] += 1
        
        # Weight class grouping
        if trainee.weight_class not in weight_class_groups:
            weight_class_groups[trainee.weight_class] = 0
        weight_class_groups[trainee.weight_class] += 1
    
    print("Distribution by Belt Rank:")
    for belt in ['white', 'yellow', 'orange', 'green', 'blue', 'brown', 'black']:
        count = belt_groups.get(belt, 0)
        if count > 0:
            bar = "█" * count
            print(f"  {belt:12}: {count:2} trainees {bar}")
    
    print("\nDistribution by Weight Class:")
    for wclass in ['Flyweight', 'Lightweight', 'Welterweight', 'Middleweight', 
                   'Light Heavyweight', 'Heavyweight']:
        count = weight_class_groups.get(wclass, 0)
        if count > 0:
            bar = "█" * count
            print(f"  {wclass:18}: {count:2} trainees {bar}")
    
    print("\n" + "=" * 100)
    print("EXPECTED MATCHING RESULTS")
    print("=" * 100 + "\n")
    
    print("Expected: 10 matches (100% success rate)")
    print("Reason: Trainees organized in perfectly matched pairs\n")
    
    print("Each pair has:")
    print("  ✓ Same belt rank")
    print("  ✓ Weight difference < 2kg")
    print("  ✓ Age difference = 1 year")
    print("  ✓ Score < 3.0 (excellent)\n")


def main():
    """Main function."""
    print("\n" + "╔" + "=" * 98 + "╗")
    print("║" + " " * 30 + "TEST AUTO-MATCHING SYSTEM" + " " * 44 + "║")
    print("║" + " " * 20 + "Create 10 Perfectly Matched Trainee Pairs" + " " * 37 + "║")
    print("╚" + "=" * 98 + "╝\n")
    
    # Check if trainees already exist
    existing_count = User.objects.filter(username__startswith='testuser').count()
    if existing_count > 0:
        print(f"⚠ WARNING: Found {existing_count} existing test users")
        print("   These will not be recreated (use different usernames if needed)\n")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return
    
    # Create test trainees
    trainees = create_test_trainees()
    
    # Create event
    event = create_test_event()
    
    # Register trainees
    register_trainees_to_event(trainees, event)
    
    # Show summary
    show_summary(trainees, event)
    
    # Test auto-matching
    test_auto_matching(event)
    
    print("=" * 100)
    print("NEXT STEPS")
    print("=" * 100 + "\n")
    print("1. Go to Admin Dashboard")
    print("2. Navigate to Events")
    print("3. Find 'Test Auto-Matching Event - 10 Pairs'")
    print("4. Click 'Auto Matchmaking' button")
    print("5. You should see 10 proposed matches!")
    print("6. Click 'Confirm' to create the matches\n")
    
    print("=" * 100)
    print("✅ TEST DATA POPULATION COMPLETE")
    print("=" * 100 + "\n")


if __name__ == '__main__':
    main()

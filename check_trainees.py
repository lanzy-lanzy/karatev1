#!/usr/bin/env python
"""
Quick script to check trainee status and weight classes.
"""
import os
import sys
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'karate.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from core.models import Trainee, Event, EventRegistration
from core.services.matchmaking import MatchmakingService, are_belts_adjacent

print("=" * 100)
print("TRAINEE WEIGHT CLASS ANALYSIS")
print("=" * 100)

# Get all active trainees
trainees = Trainee.objects.filter(archived=False).select_related('profile__user')
print(f"\nTotal active trainees: {trainees.count()}\n")

if trainees.count() == 0:
    print("No active trainees found in database.")
    sys.exit(0)

# Show all trainees with their weight classes
print(f"{'Name':<30} {'Belt':<12} {'Weight':<10} {'Weight Class':<20} {'Age':<8}")
print("-" * 100)

weight_class_dist = {}
belt_dist = {}

for trainee in trainees:
    name = trainee.profile.user.get_full_name() or trainee.profile.user.username
    belt = trainee.belt_rank
    weight = float(trainee.weight)
    wclass = trainee.weight_class or "NOT SET"
    age = trainee.age or 0
    
    print(f"{name:<30} {belt:<12} {weight:<10.2f} {wclass:<20} {age:<8}")
    
    # Collect stats
    if wclass != "NOT SET":
        weight_class_dist[wclass] = weight_class_dist.get(wclass, 0) + 1
    belt_dist[belt] = belt_dist.get(belt, 0) + 1

print("\n" + "=" * 100)
print("WEIGHT CLASS DISTRIBUTION")
print("=" * 100)
for wclass in ['Flyweight', 'Lightweight', 'Welterweight', 'Middleweight', 'Light Heavyweight', 'Heavyweight']:
    count = weight_class_dist.get(wclass, 0)
    bar = "█" * count if count > 0 else "░"
    print(f"{wclass:<18}: {count:2} trainees {bar}")

print("\n" + "=" * 100)
print("BELT RANK DISTRIBUTION")
print("=" * 100)
for belt in ['white', 'yellow', 'orange', 'green', 'blue', 'brown', 'black']:
    count = belt_dist.get(belt, 0)
    bar = "█" * count if count > 0 else "░"
    print(f"{belt:<12}: {count:2} trainees {bar}")

# Check events with registered trainees
print("\n" + "=" * 100)
print("EVENTS WITH REGISTERED TRAINEES")
print("=" * 100)

events = Event.objects.filter(registrations__status='registered').distinct()
print(f"\nTotal events with registrations: {events.count()}\n")

for event in events:
    registrations = EventRegistration.objects.filter(
        event=event,
        status='registered'
    ).select_related('trainee')
    
    event_trainees = [reg.trainee for reg in registrations]
    print(f"\n📋 Event: {event.name} ({event.event_date})")
    print(f"   Registered: {len(event_trainees)} trainees")
    
    # Analyze matchmaking for this event
    service = MatchmakingService()
    
    # Count valid pairings
    valid_pairs = []
    for i, t1 in enumerate(event_trainees):
        for t2 in event_trainees[i+1:]:
            if service._is_valid_pairing(t1, t2):
                valid_pairs.append((t1, t2))
    
    total_pairs = (len(event_trainees) * (len(event_trainees) - 1)) // 2
    
    print(f"   Valid pairings: {len(valid_pairs)}/{total_pairs}")
    
    if valid_pairs:
        print(f"   Sample valid pairs:")
        for t1, t2 in valid_pairs[:3]:
            wdiff = abs(t1.weight - t2.weight)
            age_diff = abs((t1.age or 0) - (t2.age or 0))
            print(f"     - {t1.profile.user.get_full_name():<20} vs {t2.profile.user.get_full_name():<20} (Δweight: {wdiff:.1f}kg, Δage: {age_diff}yr)")
    else:
        print(f"   ⚠ WARNING: No valid pairings could be created!")
    
    # Try to generate proposed matches
    try:
        proposed = service.auto_match(event.id)
        print(f"   Proposed matches: {len(proposed)}")
    except Exception as e:
        print(f"   Error generating matches: {e}")

print("\n" + "=" * 100)

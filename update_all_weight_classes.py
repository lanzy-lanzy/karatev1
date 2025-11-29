#!/usr/bin/env python
"""
Script to update weight classes for all trainees in the database.
Can be run standalone or imported.

Usage:
    python update_all_weight_classes.py
"""
import os
import sys
import django
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'karate.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from core.models import Trainee


def update_weight_classes():
    """Update weight classes for all active trainees."""
    
    print("\n" + "=" * 100)
    print("WEIGHT CLASS UPDATE PROCESS")
    print("=" * 100)
    
    # Get all active trainees
    trainees = Trainee.objects.filter(archived=False).select_related('profile__user')
    total = trainees.count()
    
    print(f"\nProcessing {total} active trainees...\n")
    
    if total == 0:
        print("No active trainees found.")
        return
    
    # Statistics
    updated_count = 0
    weight_class_distribution = {}
    belt_distribution = {}
    
    # Update each trainee
    for idx, trainee in enumerate(trainees, 1):
        name = trainee.profile.user.get_full_name() or trainee.profile.user.username
        
        # Get current values
        old_class = trainee.weight_class or "NOT SET"
        weight = float(trainee.weight)
        belt = trainee.belt_rank
        
        # Save to trigger auto-calculation
        trainee.save()
        
        # Get new value
        new_class = trainee.weight_class
        
        # Update distributions
        if new_class not in weight_class_distribution:
            weight_class_distribution[new_class] = 0
        weight_class_distribution[new_class] += 1
        
        if belt not in belt_distribution:
            belt_distribution[belt] = 0
        belt_distribution[belt] += 1
        
        # Log if changed
        status = "✓ UPDATED" if old_class != new_class else "→ Same"
        updated_count += 1 if old_class != new_class else 0
        
        # Print progress
        print(f"[{idx:3d}/{total:3d}] {status:12} | {name:30} | "
              f"Weight: {weight:6.2f}kg | Belt: {belt:8} | Class: {new_class:18}")
    
    # Print summary
    print("\n" + "=" * 100)
    print("SUMMARY")
    print("=" * 100)
    
    print(f"\nTotal trainees processed: {total}")
    print(f"Total updated: {updated_count}")
    print(f"Already correct: {total - updated_count}")
    
    # Weight class distribution
    print("\n📊 Weight Class Distribution:")
    print("-" * 50)
    weight_classes = [
        'Flyweight',
        'Lightweight', 
        'Welterweight',
        'Middleweight',
        'Light Heavyweight',
        'Heavyweight'
    ]
    
    for wclass in weight_classes:
        count = weight_class_distribution.get(wclass, 0)
        percentage = (count / total * 100) if total > 0 else 0
        bar = "█" * count
        print(f"  {wclass:18}: {count:3} trainees ({percentage:5.1f}%) {bar}")
    
    # Belt distribution
    print("\n🥋 Belt Rank Distribution:")
    print("-" * 50)
    belts = ['white', 'yellow', 'orange', 'green', 'blue', 'brown', 'black']
    
    for belt in belts:
        count = belt_distribution.get(belt, 0)
        percentage = (count / total * 100) if total > 0 else 0
        bar = "█" * count
        print(f"  {belt:12}: {count:3} trainees ({percentage:5.1f}%) {bar}")
    
    print("\n" + "=" * 100)
    print("✓ WEIGHT CLASS UPDATE COMPLETE")
    print("=" * 100 + "\n")


def verify_weight_classes():
    """Verify that all trainees have weight classes."""
    
    print("\n" + "=" * 100)
    print("WEIGHT CLASS VERIFICATION")
    print("=" * 100)
    
    # Check for missing weight classes
    missing = Trainee.objects.filter(archived=False, weight_class='').count()
    without_dob = Trainee.objects.filter(archived=False, profile__date_of_birth__isnull=True).count()
    
    total = Trainee.objects.filter(archived=False).count()
    
    print(f"\nTotal active trainees: {total}")
    print(f"Trainees WITH weight class: {total - missing} ✓")
    print(f"Trainees WITHOUT weight class: {missing}", "✗" if missing > 0 else "✓")
    print(f"Trainees WITHOUT date of birth: {without_dob}", "(Note: Age-based matching will be limited)")
    
    if missing > 0:
        print("\n⚠ Trainees missing weight class:")
        print("-" * 100)
        for trainee in Trainee.objects.filter(archived=False, weight_class=''):
            name = trainee.profile.user.get_full_name() or trainee.profile.user.username
            print(f"  - {name} (Weight: {trainee.weight}kg, Belt: {trainee.belt_rank})")
    
    print("\n" + "=" * 100 + "\n")


def show_weight_class_boundaries():
    """Display weight class boundaries."""
    
    print("\n" + "=" * 100)
    print("WEIGHT CLASS BOUNDARIES")
    print("=" * 100)
    
    print("\nWeight Class System:")
    print("-" * 50)
    
    boundaries = [
        (Decimal('50'), 'Flyweight', 'Up to 50 kg'),
        (Decimal('60'), 'Lightweight', '50 - 60 kg'),
        (Decimal('70'), 'Welterweight', '60 - 70 kg'),
        (Decimal('80'), 'Middleweight', '70 - 80 kg'),
        (Decimal('90'), 'Light Heavyweight', '80 - 90 kg'),
        (Decimal('999'), 'Heavyweight', '90+ kg'),
    ]
    
    for boundary, name, range_str in boundaries:
        print(f"  {name:18} | {range_str:15}")
    
    print("\n" + "=" * 100 + "\n")


if __name__ == '__main__':
    # Show boundaries first
    show_weight_class_boundaries()
    
    # Update all weight classes
    update_weight_classes()
    
    # Verify the update
    verify_weight_classes()
    
    print("✓ Process complete!")

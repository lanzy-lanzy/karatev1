#!/usr/bin/env python
"""
Test script to create a sample evaluation and verify it displays in trainee dashboard.
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'karate.settings')
django.setup()

from core.models import TraineeEvaluation, Trainee
from django.contrib.auth.models import User

# Get the first active trainee
trainee = Trainee.objects.filter(status='active').first()

if not trainee:
    print("No active trainees found. Please create a trainee first.")
    exit(1)

# Get an admin user or create one
admin_user = User.objects.filter(is_superuser=True).first()
if not admin_user:
    print("No admin user found. Creating one...")
    admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')

# Create an evaluation with belt scoring
evaluation = TraineeEvaluation.objects.create(
    trainee=trainee,
    evaluator=admin_user,
    # Old rating fields (optional now)
    technique=2,
    speed=3,
    strength=3,
    flexibility=2,
    discipline=4,
    spirit=3,
    overall_rating=3,
    # New belt scoring fields
    attendance_score=85,
    sparring_score=90,
    achievement_score=80,
    performance_score=88,
    total_belt_points=round((85 * 0.10) + (90 * 0.20) + (80 * 0.10) + (88 * 0.10)),
    # Assessment info
    comments="Great performance in this evaluation!",
    strengths="Strong sparring technique, excellent discipline",
    areas_for_improvement="Work on flexibility and footwork",
    recommendations="Continue practicing sparring drills daily",
    status='completed'
)

print("[SUCCESS] Evaluation created successfully!")
print(f"  Trainee: {trainee.profile.user.get_full_name() or trainee.profile.user.username}")
print(f"  Attendance Score: {evaluation.attendance_score}")
print(f"  Sparring Score: {evaluation.sparring_score}")
print(f"  Achievement Score: {evaluation.achievement_score}")
print(f"  Performance Score: {evaluation.performance_score}")
print(f"  Total Belt Points: {evaluation.total_belt_points}")
print(f"  Created: {evaluation.evaluated_at}")
print()
print("You should now see this in the trainee's dashboard under 'Recent Evaluations'")

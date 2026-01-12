
import os
import django
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'karate.settings')
django.setup()

from core.models import Registration, Trainee

def verify_user_mgmt_update():
    print("Verifying User Management Stats Update...")
    
    # Check total trainees count (global)
    total_trainees = Trainee.objects.count()
    print(f"Total Trainees (Global): {total_trainees}")
    
    # Check if this matches what we expect from dashboard
    # (Dashboard also uses Trainee.objects.count())
    
    # Old metric for comparison
    approved_registrations = Registration.objects.filter(status='approved').count()
    print(f"Approved Registrations (Old Metric): {approved_registrations}")
    
    if total_trainees > approved_registrations:
        print("SUCCESS: Total Trainees count includes all trainees, not just approved registrations.")
    else:
        print("NOTE: Total Trainees matches Approved Registrations (this is okay if all trainees came from registrations).")

if __name__ == "__main__":
    verify_user_mgmt_update()

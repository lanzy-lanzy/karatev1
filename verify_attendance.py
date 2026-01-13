import os
import django
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'karate.settings')
from django.conf import settings
# Configure settings if not already configured
if not settings.configured:
    django.setup()
    # Add testserver to ALLOWED_HOSTS for testing
    settings.ALLOWED_HOSTS += ['testserver']
else:
    django.setup()
    settings.ALLOWED_HOSTS += ['testserver']

from django.test import Client, RequestFactory
from django.contrib.auth.models import User
from core.models import Trainee, UserProfile, Attendance, TraineeEvaluation

def run_verification():
    print("Setting up test environment...")
    
    # Create Admin User
    admin_user, _ = User.objects.get_or_create(username='admin_test', email='test@example.com')
    admin_user.set_password('password')
    admin_user.is_superuser = True
    admin_user.is_staff = True
    admin_user.save()
    
    # Create Profile for Admin (required by decorators usually)
    UserProfile.objects.get_or_create(user=admin_user, role='admin')

    # Create Trainee
    user = User.objects.create_user(username='trainee_test', email='trainee@example.com', password='password')
    profile = UserProfile.objects.create(user=user, role='trainee', date_of_birth='2000-01-01')
    trainee = Trainee.objects.create(profile=profile, belt_rank='white', weight=60)
    
    print(f"Created trainee: {trainee}")

    # Create Attendance Records
    # Goal: 50% attendance (18 days out of 36) in last 90 days.
    # 36 is the denominator. So 18 present days.
    
    today = timezone.now().date()
    for i in range(18):
        Attendance.objects.create(
            trainee=trainee,
            date=today - timedelta(days=i),
            status='present'
        )
    
    print(f"Created 18 attendance records.")
    
    # Test Evaluation Creation Logic (via logic simulation or client)
    # Since logic is in view, we'll use Client to post data
    
    c = Client()
    c.force_login(admin_user)
    
    print("Submitting evaluation creation...")
    response = c.post('/admin/evaluations/add/', {
        'trainee': trainee.id,
        'technique': 3,
        'speed': 3,
        'strength': 3,
        'flexibility': 3,
        'discipline': 3,
        'spirit': 3,
        'overall_rating': 3,
        'sparring_score': 80,
        'achievement_score': 80,
        'performance_score': 80,
        # attendance_score is omitted to test auto-calculation
    })
    
    if response.status_code != 302:
        print(f"Failed to create evaluation. Status: {response.status_code}")
        # Try to extract exception info from traceback in content if debug is on
        content = response.content.decode()
        if "Traceback" in content:
            import re
            match = re.search(r"Tracebackn(.*?)(?:</div>|</body>)", content, re.DOTALL)
            if match:
                 print("Traceback found:")
                 print(match.group(1)[:1000]) # Print first 1000 chars of traceback
            else:
                 print("Traceback not found in content, printing first 500 chars:")
                 print(content[:500])
        else:
             print(content[:500])
    else:
        print("Evaluation created successfully (redirected).")
        
        # Verify Score
        evaluation = TraineeEvaluation.objects.get(trainee=trainee)
        print(f"Attendance Score: {evaluation.attendance_score}")
        
        expected_score = int((18 / 36) * 100) # 50
        if evaluation.attendance_score == expected_score:
            print("SUCCESS: Attendance score matching expected value (50).")
        else:
            print(f"FAILURE: Expected {expected_score}, got {evaluation.attendance_score}")

    # Cleanup
    trainee.delete()
    user.delete()
    admin_user.delete()

if __name__ == '__main__':
    try:
        run_verification()
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

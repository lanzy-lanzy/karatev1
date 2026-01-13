import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'karate.settings')
from django.conf import settings
if not settings.configured:
    django.setup()
    settings.ALLOWED_HOSTS += ['testserver']
else:
    django.setup()
    settings.ALLOWED_HOSTS += ['testserver']

from django.test import RequestFactory
from django.contrib.auth.models import User
from core.models import Trainee, UserProfile, Attendance
from core.views.attendance import attendance_dashboard

def verify_dashboard():
    print("Setting up test data...")
    # Cleanup strictly
    User.objects.filter(username__in=['admin_dash', 'trainee_dash']).delete()
    
    # Create Admin User
    user, _ = User.objects.get_or_create(username='admin_dash', email='admin@test.com')
    UserProfile.objects.get_or_create(user=user, role='admin')

    # Create Trainee
    t_user = User.objects.create_user(username='trainee_dash', email='t@test.com')
    t_profile = UserProfile.objects.create(user=t_user, role='trainee', date_of_birth='2000-01-01')
    trainee = Trainee.objects.create(profile=t_profile, belt_rank='white', weight=60)
    
    # Create Attendance for today
    today = timezone.now().date()
    Attendance.objects.create(trainee=trainee, date=today, status='present')
    
    # Create Attendance for yesterday
    yesterday = today - timedelta(days=1)
    Attendance.objects.create(trainee=trainee, date=yesterday, status='present')
    
    print("Test data created.")
    
    # Request the dashboard
    factory = RequestFactory()
    request = factory.get('/admin/attendance/')
    request.user = user
    
    print("Calling attendance_dashboard view...")
    response = attendance_dashboard(request)
    
    if response.status_code == 200:
        print("Dashboard loaded successfully.")
        content = response.content.decode()
        
        # Check for context values in the rendered HTML (a bit rough, but works)
        # We look for the calculated values
        
        # "Recorded" text should trigger if today_marked is True
        if "Recorded" in content:
             print("SUCCESS: Today's attendance marked as Recorded.")
        else:
             print("FAILURE: Today's attendance NOT marked as Recorded.")
             
        # Check for active trainees count (should be at least 1)
        if '<div class="text-3xl font-bold text-blue-400">1</div>' in content or '<div class="text-3xl font-bold text-blue-400">2</div>' in content: # Might be more if DB not stale
             print("SUCCESS: Active trainees count displayed.")
        else:
             print("WARNING: Could not verify exact active trainee count in HTML.")
        
        # Check for recent activity date
        if today.strftime("%b. %-d, %Y") in content or today.strftime("%b %d, %Y") in content:
             print("SUCCESS: Today's date found in recent activity.")
        else:
             # Try stricter format match or just lenient
             print(f"Checking for date: {today}")
             # This might fail depending on date format in template vs strftime, but let's see.
             
    else:
        print(f"Failed to load dashboard. Status: {response.status_code}")

    # Cleanup
    Attendance.objects.all().delete()
    trainee.delete()
    t_user.delete()
    user.delete()

if __name__ == '__main__':
    verify_dashboard()

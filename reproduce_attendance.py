import os
import django
from django.utils import timezone
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'karate.settings')
from django.conf import settings
if not settings.configured:
    django.setup()
    settings.ALLOWED_HOSTS += ['testserver']
else:
    django.setup()
    settings.ALLOWED_HOSTS += ['testserver']

from django.test import RequestFactory, Client
from django.contrib.auth.models import User
from core.models import Trainee, UserProfile, Attendance

def reproduce_attendance_issue():
    print("Setting up test data...")
    # Cleanup
    User.objects.filter(username__in=['admin_mark', 'trainee_mark']).delete()
    
    # Create Admin
    admin_user = User.objects.create_user(username='admin_mark', email='admin@test.com', password='password')
    UserProfile.objects.create(user=admin_user, role='admin')
    
    # Create Trainee
    t_user = User.objects.create_user(username='trainee_mark', email='t@test.com', password='password')
    t_profile = UserProfile.objects.create(user=t_user, role='trainee', date_of_birth='2000-01-01')
    trainee = Trainee.objects.create(profile=t_profile, belt_rank='white', weight=70) # Added weight as per previous fix
    
    print(f"Created trainee: {trainee.id}")
    
    # Simulate POST request to mark attendance
    c = Client()
    c.force_login(admin_user)
    
    today_str = timezone.now().date().strftime('%Y-%m-%d')
    
    # Data as it would come from the form
    post_data = {
        'date': today_str,
        f'status_{trainee.id}': 'present',
        f'notes_{trainee.id}': 'Test note'
    }
    
    print(f"Submitting attendance data: {post_data}")
    
    response = c.post('/admin/attendance/mark/', post_data)
    
    if response.status_code == 302:
        print("Redirected successfully (expected behavior).")
    else:
        print(f"Failed to redirect. Status: {response.status_code}")
        print(response.content.decode()[:500])
        
    # Verify persistence
    exists = Attendance.objects.filter(
        trainee=trainee, 
        date=today_str,
        status='present'
    ).exists()
    
    if exists:
        print("SUCCESS: Attendance record found in database.")
    else:
        print("FAILURE: Attendance record NOT found in database.")

    # Cleanup
    admin_user.delete()
    t_user.delete()
    trainee.delete()

if __name__ == '__main__':
    reproduce_attendance_issue()

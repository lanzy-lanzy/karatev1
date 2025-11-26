"""
Management command to create test users for different roles.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import UserProfile, Trainee, Judge
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Create test users for Admin, Trainee, and Judge roles'

    def handle(self, *args, **options):
        # Test Admin User
        admin_user, created = User.objects.get_or_create(
            username='admin_user',
            defaults={
                'email': 'admin@blackcobra.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': False,
            }
        )
        if created:
            admin_user.set_password('Admin@12345')
            admin_user.save()
        
        admin_profile, _ = UserProfile.objects.get_or_create(
            user=admin_user,
            defaults={
                'role': 'admin',
                'phone': '+1-234-567-8901',
                'address': '123 Dojo Street, Karate City, KC 12345',
            }
        )
        self.stdout.write(
            self.style.SUCCESS('[+] Admin user created: admin_user / Admin@12345')
        )

        # Test Trainee User
        trainee_user, created = User.objects.get_or_create(
            username='trainee_user',
            defaults={
                'email': 'trainee@blackcobra.com',
                'first_name': 'John',
                'last_name': 'Trainee',
            }
        )
        if created:
            trainee_user.set_password('Trainee@12345')
            trainee_user.save()
        
        trainee_profile, _ = UserProfile.objects.get_or_create(
            user=trainee_user,
            defaults={
                'role': 'trainee',
                'phone': '+1-345-678-9012',
                'address': '456 Martial Road, Fight Town, FT 23456',
                'date_of_birth': datetime(2000, 5, 15).date(),
            }
        )

        # Create trainee details
        trainee, _ = Trainee.objects.get_or_create(
            profile=trainee_profile,
            defaults={
                'belt_rank': 'white',
                'weight': 70.5,
                'emergency_contact': 'Jane Trainee',
                'emergency_phone': '+1-345-678-9099',
                'status': 'active',
                'joined_date': datetime.now() - timedelta(days=180),
            }
        )
        self.stdout.write(
            self.style.SUCCESS('[+] Trainee user created: trainee_user / Trainee@12345')
        )

        # Test Judge User
        judge_user, created = User.objects.get_or_create(
            username='judge_user',
            defaults={
                'email': 'judge@blackcobra.com',
                'first_name': 'Master',
                'last_name': 'Judge',
            }
        )
        if created:
            judge_user.set_password('Judge@12345')
            judge_user.save()
        
        judge_profile, _ = UserProfile.objects.get_or_create(
            user=judge_user,
            defaults={
                'role': 'judge',
                'phone': '+1-456-789-0123',
                'address': '789 Championship Ave, Victory City, VC 34567',
                'date_of_birth': datetime(1980, 3, 20).date(),
            }
        )

        # Create judge details
        judge, _ = Judge.objects.get_or_create(
            profile=judge_profile,
            defaults={
                'certification_level': 'national',
                'certification_date': datetime(2010, 1, 15).date(),
            }
        )
        self.stdout.write(
            self.style.SUCCESS('[+] Judge user created: judge_user / Judge@12345')
        )

        self.stdout.write(
            self.style.SUCCESS('\n[OK] All test users created successfully!\n')
        )
        self.stdout.write(
            self.style.WARNING('Test Credentials:\n')
        )
        self.stdout.write(
            '  Admin:   admin_user / Admin@12345\n'
            '  Trainee: trainee_user / Trainee@12345\n'
            '  Judge:   judge_user / Judge@12345'
        )

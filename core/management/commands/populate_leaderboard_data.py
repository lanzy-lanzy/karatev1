from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import (
    Trainee, UserProfile, TraineePoints, Leaderboard, Event, 
    EventRegistration, Match, MatchResult, Judge, MatchJudge, BeltRankThreshold
)
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the leaderboard with test data'

    def handle(self, *args, **options):
        self.stdout.write('Starting leaderboard data population...')
        
        # Step 1: Create additional test trainees if needed
        self.create_test_trainees()
        
        # Step 2: Create test event
        event = self.create_test_event()
        
        # Step 3: Register trainees to event
        self.register_trainees_to_event(event)
        
        # Step 4: Create matches
        matches = self.create_test_matches(event)
        
        # Step 5: Record match results and award points
        self.record_match_results(matches)
        
        # Step 6: Update leaderboards
        self.update_leaderboards()
        
        self.stdout.write(self.style.SUCCESS('SUCCESS: Leaderboard data populated successfully!'))
    
    def create_test_trainees(self):
        """Create additional test trainees if they don't exist."""
        self.stdout.write('Creating test trainees...')
        
        test_trainees = [
            {
                'username': 'trainee_john',
                'first_name': 'John',
                'last_name': 'Karate',
                'email': 'john@blackcobra.com',
                'belt_rank': 'white',
                'weight': 70.5,
            },
            {
                'username': 'trainee_sarah',
                'first_name': 'Sarah',
                'last_name': 'Warrior',
                'email': 'sarah@blackcobra.com',
                'belt_rank': 'yellow',
                'weight': 65.0,
            },
            {
                'username': 'trainee_mike',
                'first_name': 'Mike',
                'last_name': 'Champion',
                'email': 'mike@blackcobra.com',
                'belt_rank': 'orange',
                'weight': 85.5,
            },
            {
                'username': 'trainee_anna',
                'first_name': 'Anna',
                'last_name': 'Dragon',
                'email': 'anna@blackcobra.com',
                'belt_rank': 'green',
                'weight': 60.0,
            },
            {
                'username': 'trainee_alex',
                'first_name': 'Alex',
                'last_name': 'Thunder',
                'email': 'alex@blackcobra.com',
                'belt_rank': 'blue',
                'weight': 78.5,
            },
            {
                'username': 'trainee_david',
                'first_name': 'David',
                'last_name': 'Master',
                'email': 'david@blackcobra.com',
                'belt_rank': 'brown',
                'weight': 82.0,
            },
            {
                'username': 'trainee_lisa',
                'first_name': 'Lisa',
                'last_name': 'Ninja',
                'email': 'lisa@blackcobra.com',
                'belt_rank': 'black',
                'weight': 58.5,
            },
            {
                'username': 'trainee_james',
                'first_name': 'James',
                'last_name': 'Swift',
                'email': 'james@blackcobra.com',
                'belt_rank': 'white',
                'weight': 72.0,
            },
            {
                'username': 'trainee_emma',
                'first_name': 'Emma',
                'last_name': 'Tiger',
                'email': 'emma@blackcobra.com',
                'belt_rank': 'yellow',
                'weight': 62.5,
            },
            {
                'username': 'trainee_robert',
                'first_name': 'Robert',
                'last_name': 'Phoenix',
                'email': 'robert@blackcobra.com',
                'belt_rank': 'green',
                'weight': 88.0,
            },
        ]
        
        created_count = 0
        for trainee_data in test_trainees:
            username = trainee_data.pop('username')
            email = trainee_data.pop('email')
            first_name = trainee_data.pop('first_name')
            last_name = trainee_data.pop('last_name')
            belt_rank = trainee_data.pop('belt_rank')
            weight = trainee_data.pop('weight')
            
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password='TestPassword123!'
                )
                
                profile = UserProfile.objects.create(
                    user=user,
                    role='trainee',
                    phone='+1-555-0100',
                    address='123 Test Street, Test City'
                )
                
                trainee = Trainee.objects.create(
                    profile=profile,
                    belt_rank=belt_rank,
                    weight=weight,
                    emergency_contact='Emergency Contact',
                    emergency_phone='+1-555-9999',
                    status='active'
                )
                
                # Create TraineePoints entry
                TraineePoints.objects.get_or_create(trainee=trainee)
                
                created_count += 1
                self.stdout.write(f'  - Created {first_name} {last_name}')
        
        self.stdout.write(f'  Total new trainees created: {created_count}')
    
    def create_test_event(self):
        """Create a test event."""
        self.stdout.write('Creating test event...')
        
        event, created = Event.objects.get_or_create(
            name='Spring Tournament 2025',
            defaults={
                'event_date': datetime.now().date() + timedelta(days=30),
                'location': 'BlackCobra Dojo',
                'description': 'Spring tournament for all belt ranks',
                'registration_deadline': datetime.now().date() + timedelta(days=20),
                'max_participants': 50,
                'status': 'open'
            }
        )
        
        if created:
            self.stdout.write('  - Event created')
        else:
            self.stdout.write('  - Event already exists')
        
        return event
    
    def register_trainees_to_event(self, event):
        """Register trainees to the event."""
        self.stdout.write('Registering trainees to event...')
        
        trainees = Trainee.objects.all()
        registered_count = 0
        
        for trainee in trainees:
            registration, created = EventRegistration.objects.get_or_create(
                event=event,
                trainee=trainee,
                defaults={'status': 'registered'}
            )
            
            if created:
                registered_count += 1
        
        self.stdout.write(f'  - {registered_count} trainees registered')
    
    def create_test_matches(self, event):
        """Create test matches between trainees."""
        self.stdout.write('Creating test matches...')
        
        trainees = list(Trainee.objects.all())
        matches = []
        
        # Shuffle trainees to create random pairings
        random.shuffle(trainees)
        
        # Create matches for pairs
        for i in range(0, len(trainees) - 1, 2):
            match = Match.objects.create(
                event=event,
                competitor1=trainees[i],
                competitor2=trainees[i + 1],
                scheduled_time=datetime.now() + timedelta(days=25),
                status='scheduled'
            )
            matches.append(match)
        
        self.stdout.write(f'  - {len(matches)} matches created')
        return matches
    
    def record_match_results(self, matches):
        """Record match results and award points."""
        self.stdout.write('Recording match results...')
        
        # Get a judge (or use first available)
        judge = Judge.objects.first()
        
        if not judge:
            # Create a test judge if none exists
            user = User.objects.filter(username='judge_user').first()
            if not user:
                user = User.objects.create_user(
                    username='judge_test',
                    email='judge_test@blackcobra.com',
                    password='TestPassword123!'
                )
            
            profile = UserProfile.objects.create(
                user=user,
                role='judge'
            )
            
            judge = Judge.objects.create(
                profile=profile,
                certification_level='national',
                certification_date=datetime.now().date() - timedelta(days=365),
                is_active=True
            )
        
        result_count = 0
        
        for match in matches:
            # Check if result already exists
            if not hasattr(match, 'result'):
                # Randomly determine winner
                winner = match.competitor1 if random.choice([True, False]) else match.competitor2
                
                # Generate random scores
                winner_score = random.randint(5, 10)
                loser_score = random.randint(0, 4)
                
                # Record result
                result = MatchResult.objects.create(
                    match=match,
                    judge=judge,
                    winner=winner,
                    competitor1_score=winner_score if winner == match.competitor1 else loser_score,
                    competitor2_score=winner_score if winner == match.competitor2 else loser_score,
                    notes='Test match result'
                )
                
                result_count += 1
        
        self.stdout.write(f'  - {result_count} match results recorded')
    
    def update_leaderboards(self):
        """Update leaderboard rankings."""
        self.stdout.write('Updating leaderboards...')
        
        from django.db.models import Sum
        from datetime import datetime
        
        current_year = datetime.now().year
        current_month = datetime.now().month
        
        # Clear existing leaderboards
        Leaderboard.objects.all().delete()
        
        # Update all-time leaderboard
        trainees_points = TraineePoints.objects.all().order_by('-total_points')
        
        for rank, tp in enumerate(trainees_points, 1):
            # All-time
            Leaderboard.objects.create(
                trainee=tp.trainee,
                rank=rank,
                points=tp.total_points,
                timeframe='all_time',
                belt_rank=tp.trainee.belt_rank
            )
            
            # Yearly
            Leaderboard.objects.create(
                trainee=tp.trainee,
                rank=rank,
                points=tp.total_points,
                timeframe='yearly',
                year=current_year,
                belt_rank=tp.trainee.belt_rank
            )
            
            # Monthly
            Leaderboard.objects.create(
                trainee=tp.trainee,
                rank=rank,
                points=tp.total_points,
                timeframe='monthly',
                year=current_year,
                month=current_month,
                belt_rank=tp.trainee.belt_rank
            )
        
        self.stdout.write(f'  - Leaderboards updated for {trainees_points.count()} trainees')

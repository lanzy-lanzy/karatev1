"""
Management command to fix weight classes for all trainees and analyze matchmaking.
"""
from django.core.management.base import BaseCommand
from django.db.models import Q
from decimal import Decimal
from core.models import Trainee, Event, EventRegistration, Match
from core.services.matchmaking import MatchmakingService, are_belts_adjacent


class Command(BaseCommand):
    help = 'Fix weight classes for all trainees and analyze matchmaking functionality'

    def add_arguments(self, parser):
        parser.add_argument(
            '--analyze-only',
            action='store_true',
            help='Only analyze without fixing',
        )
        parser.add_argument(
            '--event-id',
            type=int,
            help='Analyze matchmaking for specific event ID',
        )

    def handle(self, *args, **options):
        analyze_only = options.get('analyze_only', False)
        event_id = options.get('event_id')

        # Fix weight classes
        if not analyze_only:
            self.fix_weight_classes()

        # Analyze matchmaking
        self.analyze_matchmaking(event_id)

    def fix_weight_classes(self):
        """Update weight classes for all trainees."""
        self.stdout.write(self.style.WARNING('=== FIXING WEIGHT CLASSES ===\n'))
        
        trainees = Trainee.objects.filter(archived=False)
        self.stdout.write(f"Processing {trainees.count()} active trainees...\n")

        updated_count = 0
        weight_class_stats = {}

        for trainee in trainees:
            old_class = trainee.weight_class
            trainee.save()  # This triggers calculate_weight_class()
            new_class = trainee.weight_class
            
            # Track weight class distribution
            if new_class not in weight_class_stats:
                weight_class_stats[new_class] = 0
            weight_class_stats[new_class] += 1
            
            if old_class != new_class:
                updated_count += 1
                self.stdout.write(
                    f"  {trainee.profile.user.get_full_name():30} | "
                    f"Weight: {trainee.weight}kg | "
                    f"Belt: {trainee.belt_rank:8} | "
                    f"Class: {new_class:18} (was: {old_class})"
                )

        self.stdout.write(self.style.SUCCESS(f'\n✓ Updated {updated_count} trainees'))
        self.stdout.write('\n=== WEIGHT CLASS DISTRIBUTION ===')
        for wclass, count in sorted(weight_class_stats.items()):
            self.stdout.write(f"  {wclass:18}: {count:3} trainees")
        self.stdout.write('')

    def analyze_matchmaking(self, event_id=None):
        """Analyze matchmaking constraints and functionality."""
        self.stdout.write(self.style.WARNING('=== ANALYZING MATCHMAKING FUNCTIONALITY ===\n'))

        # Get events with registered trainees
        if event_id:
            events = Event.objects.filter(id=event_id)
        else:
            events = Event.objects.filter(
                registrations__status='registered'
            ).distinct()

        if not events.exists():
            self.stdout.write(self.style.ERROR('No events with registered trainees found.'))
            return

        service = MatchmakingService()

        for event in events:
            self.stdout.write(f'\n📋 Event: {event.name} ({event.event_date})')
            self.stdout.write(f'   Location: {event.location}')
            
            # Get registered trainees
            registrations = EventRegistration.objects.filter(
                event=event,
                status='registered'
            ).select_related('trainee__profile')
            
            trainees = [reg.trainee for reg in registrations]
            self.stdout.write(f'   Registered: {len(trainees)} trainees')

            if len(trainees) < 2:
                self.stdout.write('   ⚠ Not enough trainees for matching')
                continue

            # Get existing matches
            existing_matches = Match.objects.filter(
                event=event
            ).exclude(status='cancelled')
            
            self.stdout.write(f'   Existing matches: {existing_matches.count()}')

            # Show trainee breakdown
            self.show_trainee_breakdown(trainees)

            # Analyze valid pairings
            self.analyze_valid_pairings(trainees, service)

            # Generate proposed matches
            self.generate_proposed_matches(event, service)

    def show_trainee_breakdown(self, trainees):
        """Show breakdown of trainees by belt and weight class."""
        self.stdout.write('\n   📊 Trainee Breakdown:')
        
        belt_stats = {}
        weight_class_stats = {}
        
        for trainee in trainees:
            # Belt rank stats
            if trainee.belt_rank not in belt_stats:
                belt_stats[trainee.belt_rank] = 0
            belt_stats[trainee.belt_rank] += 1
            
            # Weight class stats
            if trainee.weight_class not in weight_class_stats:
                weight_class_stats[trainee.weight_class] = 0
            weight_class_stats[trainee.weight_class] += 1

        self.stdout.write('      By Belt Rank:')
        for belt in ['white', 'yellow', 'orange', 'green', 'blue', 'brown', 'black']:
            count = belt_stats.get(belt, 0)
            if count > 0:
                self.stdout.write(f'        {belt:10}: {count:2} trainees')

        self.stdout.write('      By Weight Class:')
        for wclass in ['Flyweight', 'Lightweight', 'Welterweight', 'Middleweight', 
                       'Light Heavyweight', 'Heavyweight']:
            count = weight_class_stats.get(wclass, 0)
            if count > 0:
                self.stdout.write(f'        {wclass:18}: {count:2} trainees')

    def analyze_valid_pairings(self, trainees, service):
        """Analyze what pairings are valid based on constraints."""
        self.stdout.write('\n   🔍 Constraint Analysis:')
        
        constraints = {
            'weight_adjacent': [],
            'belt_adjacent': [],
            'age_valid': [],
            'all_constraints': []
        }

        for i, t1 in enumerate(trainees):
            for t2 in trainees[i+1:]:
                weight_diff = abs(t1.weight - t2.weight)
                belt_adj = are_belts_adjacent(t1.belt_rank, t2.belt_rank)
                age1 = t1.age or 0
                age2 = t2.age or 0
                age_valid = abs(age1 - age2) <= 3

                if weight_diff <= Decimal('5.0'):
                    constraints['weight_adjacent'].append((t1, t2, weight_diff))
                
                if belt_adj:
                    constraints['belt_adjacent'].append((t1, t2))
                
                if age_valid:
                    constraints['age_valid'].append((t1, t2))
                
                if service._is_valid_pairing(t1, t2):
                    constraints['all_constraints'].append((t1, t2))

        self.stdout.write(f'      Weight within 5kg: {len(constraints["weight_adjacent"])}/{self._total_pairs(trainees)} pairs')
        self.stdout.write(f'      Belt same/adjacent: {len(constraints["belt_adjacent"])}/{self._total_pairs(trainees)} pairs')
        self.stdout.write(f'      Age within 3 years: {len(constraints["age_valid"])}/{self._total_pairs(trainees)} pairs')
        self.stdout.write(f'      ALL constraints met: {len(constraints["all_constraints"])}/{self._total_pairs(trainees)} pairs ✓')

    def generate_proposed_matches(self, event, service):
        """Generate proposed matches using the matchmaking service."""
        self.stdout.write('\n   🎯 Proposed Matches:')
        
        try:
            proposed = service.auto_match(event.id)
            
            if not proposed:
                self.stdout.write('      ⚠ No valid matches could be generated')
                return
            
            for i, match in enumerate(proposed, 1):
                self.stdout.write(
                    f'      {i}. {match.competitor1.profile.user.get_full_name():20} '
                    f'({match.competitor1.belt_rank:8}, {match.competitor1.weight}kg, {match.competitor1.weight_class:18}) vs '
                    f'{match.competitor2.profile.user.get_full_name():20} '
                    f'({match.competitor2.belt_rank:8}, {match.competitor2.weight}kg, {match.competitor2.weight_class:18}) '
                    f'[Score: {match.score:.2f}]'
                )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'      Error generating matches: {e}'))

    def _total_pairs(self, trainees):
        """Calculate total possible pairings."""
        n = len(trainees)
        return (n * (n - 1)) // 2

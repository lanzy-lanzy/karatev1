from django.core.management.base import BaseCommand
from core.models import BeltRankThreshold


class Command(BaseCommand):
    help = 'Initialize belt rank thresholds for the points system'

    def handle(self, *args, **options):
        # Define belt rank thresholds
        thresholds = [
            ('white', 0, 'Starting belt rank'),
            ('yellow', 150, 'First promotion'),
            ('orange', 350, 'Second promotion'),
            ('green', 600, 'Third promotion'),
            ('blue', 900, 'Fourth promotion'),
            ('brown', 1300, 'Fifth promotion'),
            ('black', 1800, 'Master level'),
        ]

        for belt_rank, points_required, description in thresholds:
            obj, created = BeltRankThreshold.objects.get_or_create(
                belt_rank=belt_rank,
                defaults={
                    'points_required': points_required,
                    'description': description,
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created {obj.get_belt_rank_display()} threshold at {points_required} points'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'{obj.get_belt_rank_display()} threshold already exists'
                    )
                )

        self.stdout.write(self.style.SUCCESS('Belt rank thresholds initialized successfully'))

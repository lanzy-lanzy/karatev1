from django.core.management.base import BaseCommand
from datetime import date
from core.models import Event
from core.services.notification_service import NotificationService


class Command(BaseCommand):
    help = 'Close events with expired registration deadlines'

    def handle(self, *args, **options):
        """
        Check all open events and close those that have:
        1. Passed registration deadline
        2. Reached maximum participants
        """
        today = date.today()
        
        # Get all open events
        open_events = Event.objects.filter(status='open')
        
        closed_count = 0
        for event in open_events:
            reason = event.close_registration()
            
            if reason == 'registration_deadline_passed':
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Closed "{event.name}" - Registration deadline ({event.registration_deadline}) passed'
                    )
                )
                # Create notification about deadline closure
                NotificationService.create_event_closed_notification(event, 'registration_deadline_passed')
                closed_count += 1
            
            elif reason == 'max_participants_reached':
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Closed "{event.name}" - Maximum participants ({event.max_participants}) reached'
                    )
                )
                # Create notification about max participants closure
                NotificationService.create_event_closed_notification(event, 'max_participants_reached')
                closed_count += 1
        
        if closed_count == 0:
            self.stdout.write(
                self.style.WARNING('No events needed to be closed')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'\nSuccessfully closed {closed_count} event(s)')
            )

"""
Django signals for automatic notification creation.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Event, EventRegistration, BeltRankProgress, Match, MatchResult
from core.services.notification_service import NotificationService


@receiver(post_save, sender=Event)
def notify_event_created(sender, instance, created, **kwargs):
    """
    Signal handler: Create notifications for all trainees when an event is created.
    """
    if created and instance.status != 'draft':
        # Only notify if event is not in draft status
        NotificationService.create_event_notification(instance, 'event_created')
    elif not created:
        # Event was updated
        NotificationService.create_event_notification(instance, 'event_updated')


@receiver(post_save, sender=EventRegistration)
def auto_close_event_on_registration(sender, instance, created, **kwargs):
    """
    Signal handler: Automatically close event registration if max participants reached.
    """
    if created:
        event = instance.event
        # Check if event should be closed due to max participants
        reason = event.close_registration()
        if reason == 'max_participants_reached':
            # Create notification about event closure
            NotificationService.create_event_closed_notification(event, 'max_participants_reached')


@receiver(post_save, sender=BeltRankProgress)
def notify_belt_promotion(sender, instance, created, **kwargs):
    """
    Signal handler: Create notifications when a trainee is promoted to a new belt.
    """
    if created:
        # Notify the trainee
        NotificationService.create_belt_promotion_notification(instance)
        # Notify admins
        NotificationService.notify_belt_promotion_to_admins(instance)


@receiver(post_save, sender=Match)
def notify_match_scheduled(sender, instance, created, **kwargs):
    """
    Signal handler: Create notifications when a match is scheduled.
    """
    if created:
        NotificationService.create_match_scheduled_notification(instance)


@receiver(post_save, sender=MatchResult)
def notify_match_result(sender, instance, created, **kwargs):
    """
    Signal handler: Create notifications when match results are posted.
    """
    if created:
        NotificationService.create_match_result_notification(instance)

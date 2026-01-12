"""
Notification service for managing in-app notifications.
"""
from django.contrib.auth.models import User
from core.models import Notification, Event, Trainee, BeltRankProgress


class NotificationService:
    """Service for creating and managing notifications."""
    
    @staticmethod
    def create_event_notification(event, notification_type='event_created'):
        """
        Create notifications for all trainees when an event is created/updated.
        
        Args:
            event: Event instance
            notification_type: Type of notification (event_created, event_updated)
        """
        # Get all trainee users
        trainee_users = User.objects.filter(
            profile__role='trainee',
            profile__trainee__status='active'
        )
        
        title = f"New Event: {event.name}"
        if notification_type == 'event_updated':
            title = f"Event Updated: {event.name}"
        
        message = f"{event.description or event.name}\n\nDate: {event.event_date}\nLocation: {event.location}"
        
        notifications = []
        for user in trainee_users:
            notif = Notification(
                notification_type=notification_type,
                title=title,
                message=message,
                recipient=user,
                event=event
            )
            notifications.append(notif)
        
        # Bulk create notifications
        if notifications:
            Notification.objects.bulk_create(notifications)
        
        return len(notifications)
    
    @staticmethod
    def create_belt_promotion_notification(belt_rank_progress):
        """
        Create a notification for a trainee when they are promoted.
        
        Args:
            belt_rank_progress: BeltRankProgress instance
        """
        trainee = belt_rank_progress.trainee
        user = trainee.profile.user
        
        old_belt = belt_rank_progress.get_old_belt_rank_display()
        new_belt = belt_rank_progress.get_new_belt_rank_display()
        
        title = f"Belt Promotion: {old_belt} → {new_belt}"
        message = f"Congratulations! You have been promoted from {old_belt} to {new_belt} belt.\n\nTotal Points: {belt_rank_progress.points_earned}"
        
        notification = Notification.objects.create(
            notification_type='belt_promotion',
            title=title,
            message=message,
            recipient=user,
            trainee=trainee
        )
        
        return notification
    
    @staticmethod
    def create_match_scheduled_notification(match):
        """
        Create notifications for competitors when a match is scheduled.
        
        Args:
            match: Match instance
        """
        competitors = [match.competitor1, match.competitor2]
        notifications = []
        
        for competitor in competitors:
            user = competitor.profile.user
            opponent = match.competitor2 if competitor == match.competitor1 else match.competitor1
            
            title = f"Match Scheduled: {match.event.name}"
            message = f"Your match has been scheduled!\n\nOpponent: {opponent.profile.user.get_full_name() or opponent.profile.user.username}\nDate & Time: {match.scheduled_time}\nEvent: {match.event.name}"
            
            notif = Notification(
                notification_type='match_scheduled',
                title=title,
                message=message,
                recipient=user,
                event=match.event,
                trainee=competitor
            )
            notifications.append(notif)
        
        if notifications:
            Notification.objects.bulk_create(notifications)
        
        return len(notifications)
    
    @staticmethod
    def create_match_result_notification(match_result):
        """
        Create notifications for competitors when a match result is posted.
        
        Args:
            match_result: MatchResult instance
        """
        match = match_result.match
        winner = match_result.winner
        loser = match.competitor1 if match.competitor2 == winner else match.competitor2
        
        notifications = []
        
        # Notification for winner
        winner_title = f"Match Result: Victory! - {match.event.name}"
        winner_message = f"Congratulations! You won your match!\n\nScore: {match_result.competitor1_score if match.competitor1 == winner else match_result.competitor2_score} - {match_result.competitor2_score if match.competitor1 == winner else match_result.competitor1_score}"
        
        notifications.append(Notification(
            notification_type='match_result',
            title=winner_title,
            message=winner_message,
            recipient=winner.profile.user,
            event=match.event,
            trainee=winner
        ))
        
        # Notification for loser
        loser_title = f"Match Result: Defeat - {match.event.name}"
        loser_message = f"Your match has ended.\n\nScore: {match_result.competitor1_score if match.competitor1 == loser else match_result.competitor2_score} - {match_result.competitor2_score if match.competitor1 == loser else match_result.competitor1_score}"
        
        notifications.append(Notification(
            notification_type='match_result',
            title=loser_title,
            message=loser_message,
            recipient=loser.profile.user,
            event=match.event,
            trainee=loser
        ))
        
        if notifications:
            Notification.objects.bulk_create(notifications)
        
        return len(notifications)
    
    @staticmethod
    def notify_belt_promotion_to_admins(belt_rank_progress):
        """
        Create notifications for admins when a trainee is promoted.
        
        Args:
            belt_rank_progress: BeltRankProgress instance
        """
        trainee = belt_rank_progress.trainee
        admin_users = User.objects.filter(profile__role='admin')
        
        old_belt = belt_rank_progress.get_old_belt_rank_display()
        new_belt = belt_rank_progress.get_new_belt_rank_display()
        trainee_name = trainee.profile.user.get_full_name() or trainee.profile.user.username
        
        title = f"Admin Notice: {trainee_name} Promoted"
        message = f"{trainee_name} has been promoted from {old_belt} to {new_belt} belt.\n\nTotal Points: {belt_rank_progress.points_earned}"
        
        notifications = []
        for admin_user in admin_users:
            notif = Notification(
                notification_type='belt_promotion',
                title=title,
                message=message,
                recipient=admin_user,
                trainee=trainee
            )
            notifications.append(notif)
        
        if notifications:
            Notification.objects.bulk_create(notifications)
        
        return len(notifications)
    
    @staticmethod
    def create_event_closed_notification(event, reason):
        """
        Create notifications for all trainees when an event registration closes.
        
        Args:
            event: Event instance
            reason: Reason for closure ('registration_deadline_passed' or 'max_participants_reached')
        """
        # Get all trainee users
        trainee_users = User.objects.filter(
            profile__role='trainee',
            profile__trainee__status='active'
        )
        
        if reason == 'registration_deadline_passed':
            title = f"Event Registration Closed: {event.name}"
            message = f"Registration for '{event.name}' has closed.\n\nReason: Registration deadline ({event.registration_deadline}) has passed.\n\nEvent Date: {event.event_date}"
        elif reason == 'max_participants_reached':
            title = f"Event Registration Closed: {event.name}"
            message = f"Registration for '{event.name}' has closed.\n\nReason: Maximum participants ({event.max_participants}) reached.\n\nEvent Date: {event.event_date}"
        else:
            title = f"Event Registration Closed: {event.name}"
            message = f"Registration for '{event.name}' has closed.\n\nEvent Date: {event.event_date}"
        
        notifications = []
        for user in trainee_users:
            notif = Notification(
                notification_type='event_updated',
                title=title,
                message=message,
                recipient=user,
                event=event
            )
            notifications.append(notif)
        
        # Bulk create notifications
        if notifications:
            Notification.objects.bulk_create(notifications)
        
        return len(notifications)
    
    @staticmethod
    def get_unread_notifications(user):
        """Get all unread notifications for a user."""
        return Notification.objects.filter(recipient=user, is_read=False).order_by('-created_at')
    
    @staticmethod
    def get_user_notifications(user, limit=10):
        """Get recent notifications for a user."""
        return Notification.objects.filter(recipient=user).order_by('-created_at')[:limit]
    
    @staticmethod
    def mark_notification_as_read(notification_id):
        """Mark a specific notification as read."""
        try:
            notification = Notification.objects.get(pk=notification_id)
            notification.mark_as_read()
            return True
        except Notification.DoesNotExist:
            return False
    
    @staticmethod
    def mark_all_as_read(user):
        """Mark all notifications for a user as read."""
        from django.utils import timezone
        count = Notification.objects.filter(
            recipient=user, 
            is_read=False
        ).update(is_read=True, read_at=timezone.now())
        return count

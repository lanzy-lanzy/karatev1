"""
Context processors for adding global context to templates.
"""
from core.models import Notification


def notifications(request):
    """
    Context processor to add notifications to template context.
    Available as 'notifications' in all templates.
    """
    if request.user.is_authenticated:
        user_notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
        unread_count = user_notifications.filter(is_read=False).count()
        
        return {
            'notifications': user_notifications[:10],  # Last 10 notifications
            'unread_notifications_count': unread_count,
            'all_notifications': user_notifications,
        }
    
    return {
        'notifications': [],
        'unread_notifications_count': 0,
        'all_notifications': [],
    }

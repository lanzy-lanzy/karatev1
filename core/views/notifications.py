"""
Views for handling notification-related functionality.
"""
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from core.models import Notification
from core.services.notification_service import NotificationService


@login_required
def notification_list(request):
    """Display all notifications for the current user."""
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()
    
    context = {
        'notifications': notifications,
        'unread_count': unread_count,
    }
    return render(request, 'notifications/notification_list.html', context)


@login_required
@require_http_methods(['POST'])
def mark_as_read(request, notification_id):
    """Mark a notification as read via AJAX."""
    success = NotificationService.mark_notification_as_read(notification_id)
    return JsonResponse({
        'success': success,
        'message': 'Notification marked as read' if success else 'Notification not found'
    })


@login_required
@require_http_methods(['POST'])
def mark_all_as_read(request):
    """Mark all notifications as read."""
    count = NotificationService.mark_all_as_read(request.user)
    return JsonResponse({
        'success': True,
        'count': count,
        'message': f'{count} notification(s) marked as read'
    })


@login_required
def get_unread_count(request):
    """Get unread notification count via AJAX."""
    count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    return JsonResponse({
        'unread_count': count
    })


@login_required
def get_recent_notifications(request):
    """Get recent notifications via AJAX."""
    limit = int(request.GET.get('limit', 10))
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')[:limit]
    
    notifications_data = [
        {
            'id': notif.id,
            'title': notif.title,
            'message': notif.message,
            'type': notif.notification_type,
            'is_read': notif.is_read,
            'created_at': notif.created_at.isoformat(),
        }
        for notif in notifications
    ]
    
    return JsonResponse({
        'notifications': notifications_data,
        'count': len(notifications_data)
    })

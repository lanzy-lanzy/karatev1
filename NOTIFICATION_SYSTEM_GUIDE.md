# In-App Notification System Implementation Guide

## Overview

The notification system has been fully integrated into the karate application. It automatically sends in-app notifications to trainees and admins for various events:

- **Event Creation**: All active trainees receive notifications when an admin creates a new event
- **Event Updates**: Notifications sent when event details are modified
- **Belt Promotion**: Trainees notified of promotion; admins alerted of promotions
- **Match Scheduling**: Competitors notified when matches are scheduled
- **Match Results**: Competitors notified of match outcomes

## Architecture

### Models

#### Notification Model
Located in `core/models.py`

```python
class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('event_created', 'Event Created'),
        ('event_updated', 'Event Updated'),
        ('belt_promotion', 'Belt Promotion'),
        ('match_scheduled', 'Match Scheduled'),
        ('match_result', 'Match Result'),
        ('event_reminder', 'Event Reminder'),
        ('general', 'General'),
    ]
    
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True)
    trainee = models.ForeignKey(Trainee, on_delete=models.SET_NULL, null=True, blank=True)
    
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', '-created_at']),
            models.Index(fields=['recipient', 'is_read']),
        ]
```

### Services

#### NotificationService
Located in `core/services/notification_service.py`

Provides utility methods for creating notifications:

```python
# Create event notifications for all trainees
NotificationService.create_event_notification(event, 'event_created')

# Create belt promotion notification
NotificationService.create_belt_promotion_notification(belt_rank_progress)

# Create match scheduled notification
NotificationService.create_match_scheduled_notification(match)

# Create match result notification
NotificationService.create_match_result_notification(match_result)

# Notify admins of promotion
NotificationService.notify_belt_promotion_to_admins(belt_rank_progress)

# Get unread notifications
unread = NotificationService.get_unread_notifications(user)

# Mark as read
NotificationService.mark_notification_as_read(notification_id)

# Mark all as read
NotificationService.mark_all_as_read(user)
```

### Context Processor

Located in `core/context_processors.py`

Makes notifications available in all templates:

```python
def notifications(request):
    if request.user.is_authenticated:
        return {
            'notifications': user_notifications,
            'unread_notifications_count': unread_count,
            'all_notifications': user_notifications,
        }
```

### Signals

Located in `core/signals.py`

Automatically triggers notifications:

```python
# When Event is created/updated
@receiver(post_save, sender=Event)
def notify_event_created(sender, instance, created, **kwargs)

# When Belt Promotion occurs
@receiver(post_save, sender=BeltRankProgress)
def notify_belt_promotion(sender, instance, created, **kwargs)

# When Match is scheduled
@receiver(post_save, sender=Match)
def notify_match_scheduled(sender, instance, created, **kwargs)

# When Match Result is posted
@receiver(post_save, sender=MatchResult)
def notify_match_result(sender, instance, created, **kwargs)
```

## Usage

### In Templates

#### Display Notification Widget in Header
```html
{% include "components/notification_widget.html" %}
```

The widget displays:
- Bell icon with unread count badge
- Dropdown showing last 10 notifications
- Link to view all notifications

#### Display All Notifications
```html
{% for notification in notifications %}
    <div class="notification-item">
        <h5>{{ notification.title }}</h5>
        <p>{{ notification.message }}</p>
        <small>{{ notification.created_at|date:"F j, Y g:i A" }}</small>
    </div>
{% endfor %}
```

### In Views

#### Get User's Notifications
```python
from core.services.notification_service import NotificationService

# Get last 10 notifications
notifications = NotificationService.get_user_notifications(request.user, limit=10)

# Get only unread
unread = NotificationService.get_unread_notifications(request.user)

# Mark as read
NotificationService.mark_notification_as_read(notification_id)

# Mark all as read
NotificationService.mark_all_as_read(request.user)
```

## Endpoints

### Web Views

- `GET /notifications/` - View all notifications (notification_list.html template)
- `POST /notifications/<id>/mark-as-read/` - Mark notification as read (AJAX)
- `POST /notifications/mark-all-as-read/` - Mark all as read (AJAX)

### API Endpoints (JSON)

- `GET /notifications/unread-count/` - Get unread notification count
  ```json
  {"unread_count": 5}
  ```

- `GET /notifications/recent/?limit=10` - Get recent notifications
  ```json
  {
    "notifications": [
      {
        "id": 1,
        "title": "New Event",
        "message": "...",
        "type": "event_created",
        "is_read": false,
        "created_at": "2025-11-27T10:30:00Z"
      }
    ],
    "count": 1
  }
  ```

## Admin Interface

### Managing Notifications

The admin panel includes a full Notification admin interface at `/admin/core/notification/`:

- View all notifications
- Filter by type, read status, creation date
- Search by title, recipient, or message
- Mark as read/unread (bulk actions)
- View notification details

### Notification Admin Actions

```
List Display: Title | Type | Recipient | Read Status | Created Date
Filters: Type | Read Status | Date Created
Search: Title, Recipient Username, Message
Actions: Mark as Read | Mark as Unread
```

## Event Flow

### Event Creation Notification Flow

1. Admin creates event with status != 'draft'
2. Django `post_save` signal triggered
3. `notify_event_created` handler calls `NotificationService.create_event_notification()`
4. Service queries all active trainees
5. Creates bulk `Notification` records for each trainee
6. Notifications appear in context processor for each user
7. Displayed in template via context processor

### Belt Promotion Notification Flow

1. Trainee earns points in match
2. `TraineePoints.check_belt_rank_promotion()` auto-promotes trainee
3. Creates `BeltRankProgress` record
4. Django `post_save` signal triggered
5. Dual notifications created:
   - `create_belt_promotion_notification()` → Notify trainee
   - `notify_belt_promotion_to_admins()` → Notify all admins
6. Notifications appear in UI immediately

### Match Scheduling Notification Flow

1. Admin schedules match
2. `Match` object created
3. Django `post_save` signal triggered
4. `notify_match_scheduled()` handler calls service
5. Creates notification for both competitors
6. Notifications appear in competitor dashboards

## Integration Points

### Already Integrated

✅ Event creation (admin.py `event_add` view)
✅ Event updates (admin.py `event_edit` view)
✅ Belt rank changes (admin.py `trainee_edit` view)
✅ All Django admin operations

### Ready for Integration

The notification system is automatically integrated via signals. These models trigger notifications on `post_save`:

- `Event` - Creates notifications
- `BeltRankProgress` - Creates notifications
- `Match` - Creates notifications
- `MatchResult` - Creates notifications

## Frontend Integration

### Include Widget in Base Template

Add to `templates/base.html` in the header/navbar:

```html
{% include "components/notification_widget.html" %}
```

### Add Notification Page

The template is provided at `templates/notifications/notification_list.html`

Add link in header:
```html
<a href="{% url 'notification_list' %}" class="nav-link">
    Notifications <span class="badge bg-danger">{{ unread_notifications_count }}</span>
</a>
```

### JavaScript for AJAX Updates

The notification widget includes JavaScript for marking as read without page reload.

For real-time updates, you can poll the API:

```javascript
// Poll every 30 seconds
setInterval(() => {
    fetch('/notifications/unread-count/')
        .then(r => r.json())
        .then(data => {
            // Update badge with data.unread_count
        });
}, 30000);
```

## Configuration

### Settings

Add to `karate/settings.py` (already done):

```python
TEMPLATES[0]['OPTIONS']['context_processors'].append(
    'core.context_processors.notifications'
)
```

### Database Indexes

The `Notification` model includes indexes for optimal query performance:

```python
indexes = [
    models.Index(fields=['recipient', '-created_at']),
    models.Index(fields=['recipient', 'is_read']),
]
```

## Testing

### Create Test Notification

```python
from django.contrib.auth.models import User
from core.models import Notification

user = User.objects.first()
Notification.objects.create(
    notification_type='general',
    title='Test Notification',
    message='This is a test',
    recipient=user
)
```

### Test Event Notification

```python
from core.models import Event
from datetime import date, timedelta

event = Event.objects.create(
    name='Test Event',
    event_date=date.today() + timedelta(days=7),
    location='Test Location',
    registration_deadline=date.today() + timedelta(days=5),
    max_participants=30,
    status='open'  # Not 'draft' - triggers notifications
)

# Check notifications were created
from core.models import Notification
notif_count = Notification.objects.filter(
    notification_type='event_created'
).count()
```

### Test Belt Promotion Notification

```python
from core.models import BeltRankProgress

# Create a promotion
promotion = BeltRankProgress.objects.create(
    trainee=trainee,
    old_belt_rank='white',
    new_belt_rank='yellow',
    points_earned=100
)

# Check notifications
from core.models import Notification
notif = Notification.objects.filter(
    notification_type='belt_promotion',
    trainee=trainee
).first()
assert notif is not None
```

## Performance Considerations

1. **Bulk Operations**: Uses `bulk_create()` for better performance when notifying multiple trainees
2. **Database Indexes**: Indexes on `(recipient, -created_at)` and `(recipient, is_read)` for fast queries
3. **Context Processor Caching**: Consider adding Django's cache framework for frequently accessed notifications
4. **Query Optimization**: Uses `select_related` where necessary

### Recommended Cache Configuration

```python
# Add to settings.py for caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Cache user notifications for 1 minute
from django.views.decorators.cache import cache_page
@cache_page(60)
def get_notifications(request):
    # ...
```

## Future Enhancements

1. **Real-time Notifications**: Integrate WebSockets (Django Channels) for instant updates
2. **Email Notifications**: Send email copies of important notifications
3. **Notification Preferences**: Let users choose which notifications to receive
4. **Push Notifications**: Add mobile push notification support
5. **Notification Groups**: Group similar notifications (e.g., "5 trainees registered")
6. **Archive/Delete**: Allow users to manage their notification history
7. **Templates**: Create reusable notification templates for consistency

## Troubleshooting

### Notifications Not Appearing

1. Check event status is not 'draft'
2. Verify trainees have status='active'
3. Check Django logs for signal errors
4. Verify context processor is in settings.py
5. Check browser console for JavaScript errors

### Notifications Showing Old Timestamps

Ensure `USE_TZ = True` in settings.py and TIME_ZONE is set correctly.

### Performance Issues

1. Check for missing database indexes
2. Run `python manage.py migrate` to ensure migration applied
3. Monitor slow queries in Django debug toolbar
4. Consider implementing caching for frequently accessed notifications

## Files Modified/Created

### New Files

- `core/models.py` - Added `Notification` model
- `core/services/notification_service.py` - Notification service
- `core/context_processors.py` - Template context processor
- `core/signals.py` - Signal handlers
- `core/views/notifications.py` - Notification views
- `templates/notifications/notification_list.html` - Notification page
- `templates/components/notification_widget.html` - Notification widget component

### Modified Files

- `core/admin.py` - Added `NotificationAdmin`
- `core/apps.py` - Register signals in `ready()` method
- `core/urls.py` - Added notification URL patterns
- `karate/settings.py` - Added context processor

### Database Migrations

- `core/migrations/0007_notification.py` - Creates Notification table

## Support

For issues or questions about the notification system:

1. Check this guide's troubleshooting section
2. Review the signal handlers in `core/signals.py`
3. Check notification creation in `notification_service.py`
4. Verify database migration was applied: `python manage.py migrate --list`

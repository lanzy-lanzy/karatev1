# Notification System - Quick Start

## 5-Minute Setup

### 1. Add Notification Widget to Base Template

Edit `templates/base.html` - Add to navbar/header:

```html
<div class="ms-auto">
    {% include "components/notification_widget.html" %}
</div>
```

### 2. Add Notification Page Link

```html
<a href="{% url 'notification_list' %}" class="nav-link">
    <i class="bi bi-bell"></i>
    Notifications
    {% if unread_notifications_count > 0 %}
        <span class="badge bg-danger">{{ unread_notifications_count }}</span>
    {% endif %}
</a>
```

### 3. Done!

Notifications will automatically:
- Create when admins create events → All trainees get notified
- Create when admins promote belt rank → Trainee + all admins notified
- Create when matches scheduled → Both competitors notified
- Create when match results posted → Both competitors notified

## How It Works

### For Event Creation (Already Working)

1. Admin creates event in `/admin/events/add/`
2. If status is NOT 'draft', notifications are auto-created
3. All active trainees receive notification
4. Shows in dropdown and `/notifications/` page

### For Belt Promotion (Already Working)

When editing a trainee's belt rank in `/admin/trainees/<id>/edit/`:

1. Admin changes belt_rank field
2. If BeltRankProgress is created (auto-promotion or manual):
   - Trainee gets belt promotion notification
   - All admins get notification of the promotion
3. Appears immediately in their notification widget

### Manual Belt Promotion via Django Admin

1. Go to `/admin/core/beltrank progress/`
2. Create new `BeltRankProgress` entry
3. Notifications auto-created for:
   - Trainee being promoted
   - All admins

## Viewing Notifications

### In Dropdown Widget
```
Click Bell Icon → See last 10 notifications → Click "View all notifications"
```

### Full Page
```
Go to /notifications/ → See all notifications → Mark as read individually
```

### API Endpoints

```bash
# Get unread count
curl http://localhost:8000/notifications/unread-count/

# Get recent notifications
curl http://localhost:8000/notifications/recent/?limit=10
```

## Admin Dashboard

Access at `/admin/core/notification/`:

- View all notifications
- Filter by type, read status, date
- Search by title/message
- Bulk actions: Mark as read/unread
- View who received what notification

## Key Features

✅ **Automatic**: Signals automatically create notifications  
✅ **No Configuration**: Works out of the box  
✅ **Context Processor**: Notifications available in all templates  
✅ **AJAX Ready**: Mark as read without page reload  
✅ **Indexed**: Database optimized for fast queries  
✅ **Admin Interface**: Full Django admin integration  

## Test It Out

### Test 1: Create Event Notification

1. Go to `/admin/events/add/`
2. Create event with status = "open" (not draft)
3. Login as trainee
4. Bell icon should show "1"
5. Click bell → See event notification

### Test 2: Belt Promotion Notification

1. Go to `/admin/trainees/`
2. Edit a trainee
3. Change belt_rank from 'white' to 'yellow'
4. Save
5. Login as that trainee → Bell shows notification
6. Login as admin → Bell shows "Trainee Promoted" notification

### Test 3: View All Notifications

1. Go to `/notifications/`
2. See all unread notifications
3. Click "Mark as read" button
4. Notification removes "New" badge
5. Click "Mark all as read" at top

## Files You Need

1. **Don't edit**:
   - `core/models.py` - Already has Notification model
   - `core/admin.py` - Already registered
   - `core/signals.py` - Already set up
   - `core/services/notification_service.py` - Ready to use
   - `core/context_processors.py` - Already configured
   - `karate/settings.py` - Already updated

2. **Edit to customize**:
   - `templates/base.html` - Add widget include
   - `templates/components/notification_widget.html` - Customize styling
   - `templates/notifications/notification_list.html` - Customize layout

## Common Tasks

### Get Unread Count in View
```python
from core.models import Notification

unread_count = Notification.objects.filter(
    recipient=request.user,
    is_read=False
).count()
```

### Create Manual Notification
```python
from core.models import Notification

Notification.objects.create(
    notification_type='general',
    title='Important Update',
    message='Your message here',
    recipient=user
)
```

### Mark All As Read Programmatically
```python
from core.services.notification_service import NotificationService

count = NotificationService.mark_all_as_read(request.user)
```

### Get User's Recent Notifications
```python
from core.models import Notification

notifications = Notification.objects.filter(
    recipient=request.user
).order_by('-created_at')[:10]
```

## Customization

### Change Notification Message
Edit `core/services/notification_service.py` - modify message strings in methods like:
- `create_event_notification()`
- `create_belt_promotion_notification()`
- etc.

### Change Widget Styling
Edit `templates/components/notification_widget.html` - modify CSS classes

### Change Notification Page Layout
Edit `templates/notifications/notification_list.html` - modify HTML/CSS

### Add New Notification Type
1. Add to `Notification.NOTIFICATION_TYPES` in `core/models.py`
2. Create method in `NotificationService` 
3. Create signal handler in `core/signals.py`
4. Call service in signal handler

## Production Tips

1. **Backup database before deploying**: 
   ```bash
   python manage.py dumpdata > backup.json
   ```

2. **Run migrations in production**:
   ```bash
   python manage.py migrate
   ```

3. **Monitor notifications table**:
   ```bash
   python manage.py dbshell
   SELECT COUNT(*) FROM core_notification;
   ```

4. **Archive old notifications** (optional):
   ```python
   from datetime import timedelta
   from django.utils import timezone
   from core.models import Notification
   
   old_date = timezone.now() - timedelta(days=30)
   Notification.objects.filter(created_at__lt=old_date).delete()
   ```

## Need Help?

Check `NOTIFICATION_SYSTEM_GUIDE.md` for:
- Full API documentation
- Architecture details
- Troubleshooting
- Performance optimization
- Future enhancements

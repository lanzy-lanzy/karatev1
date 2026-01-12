# Event Auto-Closure Feature - Quick Reference

## What Does It Do?
Events automatically close registration when:
1. Registration deadline date is reached
2. Maximum number of participants register

## Where Is It Implemented?

### Model Layer (`core/models.py`)
```python
event = Event.objects.get(id=1)

# Check if should close (doesn't modify)
should_close, reason = event.should_close()

# Actually close the event
reason = event.close_registration()
```

### Signals (`core/signals.py`)
Automatically triggered when trainee registers → event closes if max reached

### Admin Views (`core/views/admin.py`)
When creating or editing events → checks auto-closure conditions

### Management Command
```bash
python manage.py close_expired_events
```
Closes all open events with passed deadlines

## How to Use

### Daily Auto-Closure (Recommended)
Schedule the management command to run daily:
```bash
# Run manually anytime
python manage.py close_expired_events

# Or add to crontab for daily 1am execution
0 1 * * * cd /path/to/karate && python manage.py close_expired_events
```

### Manual Closure in Django Shell
```bash
python manage.py shell
>>> from core.models import Event
>>> event = Event.objects.get(id=1)
>>> reason = event.close_registration()
>>> print(f"Closed for reason: {reason}")
```

### Check Event Status
```python
event = Event.objects.get(id=1)
print(f"Status: {event.status}")
print(f"Participants: {event.participant_count}/{event.max_participants}")
print(f"Deadline: {event.registration_deadline}")
print(f"Open?: {event.is_registration_open}")
```

## Event Status Values
- `'draft'` - Not yet published
- `'open'` - Accepting registrations
- `'closed'` - Registration closed (auto or manual)
- `'ongoing'` - Event is happening
- `'completed'` - Event finished
- `'cancelled'` - Event cancelled

## Key Points

✅ **What It Does:**
- Automatically closes events when deadline passes
- Automatically closes events when max capacity reached
- Creates notifications to inform trainees
- Works on event creation and during edits

✅ **No Manual Action Needed:**
- Signals handle it automatically for registrations
- Management command handles deadline-based closure
- Admin views prevent invalid event creation

⚠️ **Important:**
- Closed events can still be viewed
- Admin can manually reopen events if needed
- Notifications go to all active trainees
- Prevents new registrations once closed

## Files Modified/Created

| File | Change |
|------|--------|
| `core/models.py` | Added `should_close()` and `close_registration()` methods |
| `core/signals.py` | Added `auto_close_event_on_registration` signal |
| `core/services/notification_service.py` | Added `create_event_closed_notification()` |
| `core/views/admin.py` | Updated event create/edit views |
| `core/management/commands/close_expired_events.py` | NEW - Management command |
| `run_close_expired_events.py` | NEW - Helper script |

## Troubleshooting

### Events Not Auto-Closing?
1. Check event status is 'open' (not 'draft' or 'closed')
2. Verify registration deadline is today or earlier
3. Check participant count is at or above max_participants
4. Run management command manually to test

### Signals Not Firing?
- Check signals are imported in `core/__init__.py`
- Verify Django apps are configured correctly
- Check database is accessible

### Notifications Not Showing?
- Verify trainees exist and status='active'
- Check notification model is working
- Review admin notifications page

## Performance Tips
- Schedule management command during off-hours
- Monitor database load if large participant count
- Use bulk operations for notifications (already implemented)

## Rollback
If you need to disable:
1. Comment out signal in `core/signals.py`
2. Don't call management command
3. Manually update event statuses if needed

# Event Auto-Closure Implementation

## Overview
This feature automatically closes event registration when either:
1. **Registration deadline is reached** - Registration closes on the specified deadline date
2. **Maximum participants reached** - Registration closes when the event reaches its maximum capacity

## Components

### 1. Event Model Updates (`core/models.py`)
Added two new methods to the `Event` model:

#### `should_close()`
- Checks if an event should be closed
- Returns a tuple: `(bool, reason)` where reason is one of:
  - `"registration_deadline_passed"` - deadline date has passed
  - `"max_participants_reached"` - event is at max capacity
  - `None` - event should remain open
- Does NOT modify the database, only checks conditions

#### `close_registration()`
- Automatically closes the event if conditions are met
- Sets event status to `'closed'`
- Saves changes to database
- Returns the closure reason or `None` if not closed

### 2. Event Registration Signal (`core/signals.py`)
**Signal:** `auto_close_event_on_registration`
- Triggered when a new `EventRegistration` is created
- Automatically calls `event.close_registration()`
- Creates a closure notification if max participants reached
- This ensures the event closes immediately when the last spot is filled

### 3. Event Admin Views (`core/views/admin.py`)
Both **create event** and **edit event** views now:
- Check if an event should be auto-closed when status is set to 'open'
- Display appropriate warning messages if auto-closure occurs:
  - "Event created but registration is already closed (deadline has passed)"
  - "Event created but registration is already closed (max participants reached)"
- This prevents creating/saving events that should already be closed

### 4. Management Command (`core/management/commands/close_expired_events.py`)
**Command:** `python manage.py close_expired_events`

Checks all open events and closes those that:
- Have passed their registration deadline
- Have reached maximum participants

Output shows which events were closed and why.

**Usage:**
```bash
python manage.py close_expired_events
```

### 5. Notification Service (`core/services/notification_service.py`)
**Method:** `create_event_closed_notification(event, reason)`
- Creates notifications for all active trainees when an event closes
- Messages include the reason for closure and key event details
- Called by both signals and management command

### 6. Helper Script (`run_close_expired_events.py`)
Convenience script to run the management command from command line or cron.

**Usage:**
```bash
python run_close_expired_events.py
```

## Workflow

### Scenario 1: Max Participants Reached
1. Admin creates event with max_participants=10, status='open'
2. 9 trainees register
3. 10th trainee registers
4. `EventRegistration` signal fires
5. Event closure check runs → detects max reached
6. Event status changes to 'closed'
7. Notification sent to all trainees

### Scenario 2: Registration Deadline Passes
1. Admin creates event with registration_deadline=2026-01-15, status='open'
2. Admin runs `close_expired_events` command on 2026-01-16 or later
3. Management command detects deadline passed
4. Event status changes to 'closed'
5. Notification sent to all trainees

### Scenario 3: Admin Updates Event
1. Admin edits event, sets status='open'
2. If registration_deadline or max_participants conditions are met
3. Event auto-closes with warning message

## Database Impact
- No schema changes required
- Uses existing `Event.status` field
- No new models or migrations needed

## Scheduling for Production

### Option 1: Django Management Command with Cron
```bash
# Add to crontab (runs daily at midnight)
0 0 * * * cd /path/to/karate && /path/to/venv/bin/python manage.py close_expired_events >> /var/log/karate_close_events.log 2>&1
```

### Option 2: Using Celery (if available)
Can be extended to use Celery periodic tasks for more control.

### Option 3: Cloud Scheduler
On cloud platforms (AWS, GCP, Azure), configure a scheduled job to call the management command daily.

## Configuration

No configuration needed. The feature uses existing Event model fields:
- `registration_deadline` - DateField
- `max_participants` - IntegerField
- `status` - CharField with choices

## Testing

### Manual Testing
```bash
# Test the management command
python manage.py close_expired_events

# Test via Django shell
from core.models import Event
event = Event.objects.get(id=1)
reason = event.close_registration()
print(f"Closed: {reason}")
```

### Test Scenarios

**Test 1: Deadline Passed**
1. Create event with past deadline
2. Set status to 'open'
3. Check if auto-closes with warning

**Test 2: Max Participants**
1. Create event with max_participants=2
2. Register 2 trainees
3. Check if event auto-closes after 2nd registration

**Test 3: Management Command**
1. Create multiple events with passed deadlines
2. Run `python manage.py close_expired_events`
3. Verify all are closed

## Error Handling
- Signals wrapped in try-except to prevent registration failures
- Management command logs all actions
- Admin views display clear warning messages
- Notifications only sent if users exist

## Performance Considerations
- `should_close()` is lightweight - only date comparison
- Signal only runs on registration creation (minimal overhead)
- Management command uses standard Django ORM queries
- Bulk notification creation for efficiency

## Future Enhancements
1. Add ability to re-open registration
2. Waitlist management when max reached
3. Auto-extend deadline via admin action
4. Email notifications in addition to in-app
5. Admin dashboard showing auto-closed events
6. Configuration for auto-closure behavior

## Rollback
To disable auto-closure:
1. Comment out signal in `core/signals.py`
2. Manually revert closed events to 'open'
3. Events will not auto-close until signal is re-enabled

## Support
For issues or questions, check:
- Event model documentation
- Signal handler logging
- Management command verbose output
- Notification service logs

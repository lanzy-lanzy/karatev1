# Event Auto-Closure - Developer Quick Start

## 5-Minute Overview

The feature automatically closes event registrations when:
1. **Registration deadline** passes
2. **Maximum participants** register

## Files You Need to Know

| File | Purpose | Change Type |
|------|---------|------------|
| `core/models.py` | Event model methods | Modified |
| `core/signals.py` | Auto-close on registration | Modified |
| `core/views/admin.py` | Admin form validation | Modified |
| `core/services/notification_service.py` | Send closure notifications | Modified |
| `core/management/commands/close_expired_events.py` | Batch closure command | New |
| `run_close_expired_events.py` | Helper script | New |

## Key Methods to Know

### Event Model (`core/models.py`)
```python
# Check if event should close (read-only)
should_close, reason = event.should_close()
# Returns: (True, "registration_deadline_passed") or 
#          (True, "max_participants_reached") or
#          (False, None)

# Actually close the event
reason = event.close_registration()
# Returns: "registration_deadline_passed", "max_participants_reached", or None
# Side effect: Sets event.status = 'closed' if conditions met
```

### Properties (also in Event model)
```python
event.is_registration_open  # True if registration still open
event.is_full              # True if at max participants
event.participant_count    # Number of registered trainees
```

## How the Workflow Works

### On Registration (Signal)
```
Trainee registers → EventRegistration saved → Signal fires
→ auto_close_event_on_registration() 
→ event.close_registration()
→ If max reached: Create notification
```

### On Event Edit/Create (View)
```
Admin saves event with status='open' 
→ View calls event.close_registration()
→ If already closed: Show warning, set status='closed'
```

### Daily Batch (Management Command)
```
Cron runs at 1 AM → manage.py close_expired_events
→ For all open events: Check deadline
→ If deadline passed: Close and notify
```

## Testing Locally

### Quick Test: Max Participants
```bash
# Terminal 1 - Django shell
python manage.py shell

>>> from core.models import Event
>>> from datetime import date, timedelta
>>> 
>>> # Create event with max=2
>>> event = Event.objects.create(
...     name="Test Event",
...     event_date=date.today() + timedelta(days=10),
...     location="Test",
...     registration_deadline=date.today() + timedelta(days=5),
...     max_participants=2,
...     status='open'
... )
>>> 
>>> # Get 2 trainees
>>> from core.models import Trainee
>>> trainees = Trainee.objects.all()[:2]
>>> 
>>> # Register them one by one
>>> from core.models import EventRegistration
>>> EventRegistration.objects.create(event=event, trainee=trainees[0])
>>> 
>>> event.refresh_from_db()
>>> print(f"Status after 1st reg: {event.status}")  # Still 'open'
>>> 
>>> EventRegistration.objects.create(event=event, trainee=trainees[1])
>>> 
>>> event.refresh_from_db()
>>> print(f"Status after 2nd reg: {event.status}")  # Now 'closed'!
```

### Quick Test: Management Command
```bash
python manage.py shell

>>> from core.models import Event
>>> from datetime import date, timedelta
>>> 
>>> # Create expired event
>>> Event.objects.create(
...     name="Expired Event",
...     event_date=date.today() + timedelta(days=10),
...     location="Test",
...     registration_deadline=date.today() - timedelta(days=1),  # Yesterday
...     max_participants=10,
...     status='open'
... )

# Exit shell (Ctrl+D)

python manage.py close_expired_events
# Output: "Closed 'Expired Event' - Registration deadline passed"
```

## Common Tasks

### Debug: Check Event Status
```python
from core.models import Event

event = Event.objects.get(id=1)
print(f"Status: {event.status}")
print(f"Deadline: {event.registration_deadline}")
print(f"Max: {event.max_participants}")
print(f"Current: {event.participant_count}")
print(f"Is open: {event.is_registration_open}")

should_close, reason = event.should_close()
print(f"Should close: {should_close}, reason: {reason}")
```

### Debug: Check Notifications
```python
from core.models import Notification, Event

event = Event.objects.get(id=1)
notifs = Notification.objects.filter(event=event)
print(f"Total notifications: {notifs.count()}")
for n in notifs[:5]:
    print(f"  {n.title}: {n.message[:50]}...")
```

### Debug: Run Management Command Verbosely
```bash
python manage.py close_expired_events --verbosity=2
```

### Debug: Check Signal Execution
```python
# Add logging to see if signal fires
# In core/signals.py, add print statements:
print(f"Signal fired for event {instance.event.id}")
print(f"Closure reason: {reason}")
```

## Troubleshooting

### Event Won't Close
```python
# Check conditions
event = Event.objects.get(id=1)
print(f"Status: {event.status}")  # Must be 'open'
print(f"Deadline: {event.registration_deadline} vs today")
print(f"Participants: {event.participant_count}/{event.max_participants}")

# Force close if needed
event.close_registration()
event.refresh_from_db()
print(f"New status: {event.status}")
```

### Signal Not Firing
```python
# Check import in signals.py
# Make sure EventRegistration is imported

# Test signal manually
from core.models import Event, EventRegistration
from core.signals import auto_close_event_on_registration

event = Event.objects.get(id=1)
reg = EventRegistration.objects.filter(event=event).first()

# Call signal manually to test
auto_close_event_on_registration(
    sender=EventRegistration, 
    instance=reg, 
    created=True
)
```

### Management Command Not Running
```bash
# Check if installed properly
python manage.py help close_expired_events

# Run with full output
python manage.py close_expired_events -v 2

# Check cron job
crontab -l

# Test cron environment
# Run commands as cron would
cd /path/to/karate
/path/to/venv/bin/python manage.py close_expired_events
```

## Code Patterns

### Check and Close Pattern
```python
event = Event.objects.get(id=1)

# Pattern 1: Check first
should_close, reason = event.should_close()
if should_close:
    event.close_registration()
    # reason: "registration_deadline_passed" or "max_participants_reached"

# Pattern 2: Just close (returns reason or None)
reason = event.close_registration()
if reason:
    print(f"Closed for: {reason}")
```

### Create Notification Pattern
```python
from core.services.notification_service import NotificationService

event = Event.objects.get(id=1)
NotificationService.create_event_closed_notification(
    event, 
    'max_participants_reached'  # or 'registration_deadline_passed'
)
```

## Performance Tips

- `should_close()` is fast - just date comparison
- `close_registration()` saves to DB - expect <10ms
- Signals are synchronous - register <50ms
- Use bulk_create for notifications

## Common Issues & Solutions

### Issue: Events closing unexpectedly
**Solution:** Check registration_deadline field. Remember: deadline must be in PAST to close.
```python
from datetime import date
event.registration_deadline < date.today()  # True = closes
```

### Issue: Duplicate notifications
**Solution:** Signal might fire multiple times. Check for transaction issues or signal disconnect/reconnect.

### Issue: Cron not running
**Solution:** Check crontab syntax, environment variables, working directory.
```bash
# Good crontab entry:
0 1 * * * cd /path/to/karate && /path/to/venv/bin/python manage.py close_expired_events
```

### Issue: Management command slow
**Solution:** Use --batch-size or optimize queries. Current implementation uses Django ORM efficiently.

## Adding Features

### To add re-opening:
```python
def reopen_registration(self):
    if self.status == 'closed':
        self.status = 'open'
        self.save()
        return True
    return False
```

### To add waitlist:
```python
# In EventRegistration:
class EventRegistration(models.Model):
    is_waitlisted = models.BooleanField(default=False)
    
    # Promote from waitlist when someone cancels
```

### To add email notifications:
```python
# In notification_service.py:
def send_email_notification(self, user, event, reason):
    subject = f"Event {event.name} Registration Closed"
    # Use Django email backend
```

## Useful Django Commands

```bash
# Django shell
python manage.py shell

# List all events
python manage.py shell
>>> from core.models import Event
>>> Event.objects.all()

# Check migrations needed
python manage.py makemigrations --check

# View database
sqlite3 db.sqlite3
>>> SELECT status, COUNT(*) FROM core_event GROUP BY status;

# Test management command
python manage.py close_expired_events --dry-run  # If implemented

# View logs
tail -f logs/django.log
```

## Documentation Reference

- **Full Documentation**: `EVENT_AUTO_CLOSURE_IMPLEMENTATION.md`
- **Quick Reference**: `EVENT_AUTO_CLOSURE_QUICK_REFERENCE.md`
- **Diagrams**: `EVENT_AUTO_CLOSURE_FLOW_DIAGRAM.md`
- **Testing**: `EVENT_AUTO_CLOSURE_TEST_GUIDE.md`
- **Deployment**: `EVENT_AUTO_CLOSURE_DEPLOYMENT_CHECKLIST.md`

## Next Steps

1. **Review** the code changes in the 5 files above
2. **Test** locally using the quick test examples
3. **Run** the test guide test cases
4. **Deploy** using the deployment checklist

---

**Status:** Ready to use  
**Questions?** Check the documentation files or test guide

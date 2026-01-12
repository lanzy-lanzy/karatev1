# Event Auto-Closure Feature - README

## What Does This Feature Do?

Events automatically close registration when:
1. **Registration Deadline Reached** - On the deadline date, registration closes
2. **Maximum Participants Registered** - When the last available spot is filled

## Example Scenarios

### Scenario 1: Deadline-Based Closure
```
Jan 15: Admin creates event with deadline = Jan 20
Jan 20: Registration closes automatically (0 additional action needed)
Jan 20+: Trainees cannot register, see "Registration Closed" message
```

### Scenario 2: Capacity-Based Closure  
```
Jan 15: Admin creates event, max = 10 participants
Jan 18: 9th trainee registers
Jan 18: 10th trainee registers → Event auto-closes immediately
Jan 18+: No more trainees can register
```

### Scenario 3: Pre-Closed Event
```
Jan 15: Admin tries to create event with deadline in the past
Result: Warning shown, event created but immediately closed
```

## Installation & Setup

### No Database Migration Needed ✅
This feature uses existing database fields. No new migrations required.

### Enable the Feature (Already Enabled)
The feature is built-in. Just ensure:
1. Core/signals.py is imported in core/__init__.py
2. Django apps are properly configured

### Schedule Daily Closure Check (Optional)
For deadline-based closure, schedule the management command:

```bash
# Add to crontab (runs daily at 1 AM)
0 1 * * * cd /path/to/karate && python manage.py close_expired_events
```

## Quick Start

### For Users/Admins
1. Create events normally
2. When deadline approaches or max capacity reached, events close automatically
3. Trainees receive notifications
4. Everything works automatically - no manual steps needed

### For Developers
```bash
# Test the feature
python manage.py shell

from core.models import Event
event = Event.objects.get(id=1)

# Check if should close
should_close, reason = event.should_close()

# Actually close it
reason = event.close_registration()
```

### For DevOps
```bash
# Setup (one-time)
crontab -e
# Add: 0 1 * * * cd /path/to/karate && python manage.py close_expired_events

# Monitor
tail -f /var/log/karate/close_events.log

# Test anytime
python manage.py close_expired_events
```

## File Structure

```
Modified Files:
- core/models.py (added 2 methods to Event)
- core/signals.py (added 1 signal handler)
- core/views/admin.py (updated event create/edit)
- core/services/notification_service.py (added 1 method)

New Files:
- core/management/commands/close_expired_events.py (management command)
- run_close_expired_events.py (helper script)

Documentation (9 files):
- EVENT_AUTO_CLOSURE_README.md (START HERE)
- EVENT_AUTO_CLOSURE_INDEX.md
- EVENT_AUTO_CLOSURE_SUMMARY.md
- EVENT_AUTO_CLOSURE_QUICK_REFERENCE.md
- EVENT_AUTO_CLOSURE_IMPLEMENTATION.md
- EVENT_AUTO_CLOSURE_FLOW_DIAGRAM.md
- EVENT_AUTO_CLOSURE_DEV_GUIDE.md
- EVENT_AUTO_CLOSURE_TEST_GUIDE.md
- EVENT_AUTO_CLOSURE_DEPLOYMENT_CHECKLIST.md
```

## Documentation

Start with these files in order:

1. **EVENT_AUTO_CLOSURE_README.md** (5 min) ← You are here
   - Overview
   - Quick start
   - FAQ

2. **EVENT_AUTO_CLOSURE_SUMMARY.md** (5 min)
   - What's included
   - How it works
   - Implementation overview

3. **EVENT_AUTO_CLOSURE_QUICK_REFERENCE.md** (5 min)
   - What it does
   - How to use
   - Troubleshooting

4. **EVENT_AUTO_CLOSURE_IMPLEMENTATION.md** (15 min)
   - Complete technical details
   - Workflow scenarios
   - Configuration options

5. **EVENT_AUTO_CLOSURE_DEV_GUIDE.md** (10 min)
   - For developers
   - Code examples
   - Testing examples

6. **EVENT_AUTO_CLOSURE_TEST_GUIDE.md** (60 min)
   - Comprehensive testing
   - 7 test cases
   - How to verify

7. **EVENT_AUTO_CLOSURE_DEPLOYMENT_CHECKLIST.md** (30 min)
   - Before deployment
   - Deployment steps
   - Post-deployment checks

8. **EVENT_AUTO_CLOSURE_FLOW_DIAGRAM.md** (10 min)
   - Visual diagrams
   - Architecture overview
   - Data flow

9. **EVENT_AUTO_CLOSURE_INDEX.md** (reference)
   - Complete index
   - File locations
   - Key statistics

## Key Features

✅ **Automatic Closure**
- Closes when deadline passes
- Closes when max participants register

✅ **No Manual Action**
- Works automatically via signals
- Management command for batch closure
- Admin views prevent invalid states

✅ **Notifications**
- Trainees notified of closure
- Includes closure reason
- Bulk created for efficiency

✅ **Zero Database Migration**
- Uses existing fields
- No schema changes
- Fully backward compatible

✅ **Production Ready**
- Full error handling
- Comprehensive logging
- Performance optimized

## Usage

### Management Command
```bash
# Run manually anytime
python manage.py close_expired_events

# Schedule with cron
0 1 * * * cd /path/to/karate && python manage.py close_expired_events
```

### Event Methods
```python
from core.models import Event

event = Event.objects.get(id=1)

# Check if should close (doesn't modify)
should_close, reason = event.should_close()

# Close if conditions met
reason = event.close_registration()

# Check if open
if event.is_registration_open:
    # Can register
    pass
```

## Monitoring

### View Closed Events
```python
from core.models import Event
closed = Event.objects.filter(status='closed')
print(f"Closed events: {closed.count()}")
```

### View Notifications
```python
from core.models import Notification
notifs = Notification.objects.filter(
    notification_type='event_updated'
).order_by('-created_at')[:10]
```

### Check Logs
```bash
# Cron execution logs
tail -f /var/log/karate/close_events.log

# Django logs
tail -f logs/django.log
```

## Testing

Quick local test:
```bash
python manage.py shell

# Create event with max=1
from core.models import Event
from datetime import date, timedelta
event = Event.objects.create(
    name="Test",
    event_date=date.today() + timedelta(days=10),
    location="Test",
    registration_deadline=date.today() + timedelta(days=5),
    max_participants=1,
    status='open'
)

# Register one trainee
from core.models import EventRegistration, Trainee
trainee = Trainee.objects.first()
EventRegistration.objects.create(event=event, trainee=trainee)

# Check if closed
event.refresh_from_db()
print(event.status)  # Should be 'closed'
```

See **EVENT_AUTO_CLOSURE_TEST_GUIDE.md** for comprehensive test cases.

## Troubleshooting

### Event not closing?
1. Check event status is 'open'
2. Verify conditions are met:
   - Deadline in past OR max participants reached
3. Run management command: `python manage.py close_expired_events`

### Signals not firing?
1. Verify imports in core/__init__.py
2. Check Django app configuration
3. Review console for errors

### Management command not found?
1. Verify file exists: `core/management/commands/close_expired_events.py`
2. Check Django app config
3. Run: `python manage.py help close_expired_events`

## FAQ

**Q: Will this break existing functionality?**
A: No. The feature uses existing fields and adds no breaking changes.

**Q: Do I need to run migrations?**
A: No. Zero database migrations required.

**Q: Can events be re-opened?**
A: Yes, admins can manually change status back to 'open'.

**Q: What happens to registrations when event closes?**
A: Existing registrations remain. Only new registrations are blocked.

**Q: Are trainees notified?**
A: Yes, all active trainees get notifications.

**Q: Can I customize the behavior?**
A: Yes, extend the Event model methods or modify the signal.

## Support

For questions or issues:
1. Check the documentation (9 files provided)
2. Review test cases in TEST_GUIDE.md
3. Check code comments and docstrings
4. Review deployment checklist

## Next Steps

1. **Read** EVENT_AUTO_CLOSURE_SUMMARY.md (5 min)
2. **Test** using EVENT_AUTO_CLOSURE_DEV_GUIDE.md (15 min)
3. **Deploy** using EVENT_AUTO_CLOSURE_DEPLOYMENT_CHECKLIST.md
4. **Monitor** using deployment checklist post-deployment checks

## Version

- **Version**: 1.0
- **Release Date**: January 11, 2026
- **Status**: Ready for Deployment
- **Documentation**: Complete
- **Testing**: Guide Provided

---

**Next:** Read `EVENT_AUTO_CLOSURE_SUMMARY.md`

Questions? Check the comprehensive documentation files provided.

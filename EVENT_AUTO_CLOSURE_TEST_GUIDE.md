# Event Auto-Closure Testing Guide

## Quick Test Checklist

- [ ] Deadline-based auto-closure
- [ ] Max participants auto-closure
- [ ] Admin view auto-closure detection
- [ ] Signal fires on registration
- [ ] Notifications created
- [ ] Management command executes

## Test Environment Setup

```bash
# Install dependencies (if not already installed)
pip install -r requirements.txt

# Run migrations (if needed)
python manage.py migrate

# Create test users
python manage.py create_test_users

# Start development server
python manage.py runserver
```

## Test Case 1: Deadline-Based Auto-Closure

### Objective
Verify event closes when registration deadline passes.

### Setup
```bash
# Using Django shell
python manage.py shell

>>> from core.models import Event
>>> from datetime import date, timedelta
>>> 
>>> # Create event with deadline 1 day ago
>>> event = Event.objects.create(
...     name="Test Event - Deadline",
...     event_date=date.today() + timedelta(days=10),
...     location="Test Location",
...     registration_deadline=date.today() - timedelta(days=1),  # Yesterday
...     max_participants=10,
...     status='open'
... )
>>> print(f"Created event: {event.name}, ID: {event.id}")
```

### Test Steps
1. Go to admin: http://127.0.0.1:8000/admin/events/
2. Search for "Test Event - Deadline"
3. Edit the event
4. Change status to "Open for Registration"
5. Click "Update Event"

### Expected Result
- ✅ Warning message displays: "registration has been automatically closed due to deadline"
- ✅ Event status changes to "Registration Closed"
- ✅ No save error occurs

### Verification
```bash
>>> event.refresh_from_db()
>>> print(f"Event status: {event.status}")  # Should be 'closed'
```

---

## Test Case 2: Max Participants Auto-Closure on Registration

### Objective
Verify event closes when maximum participants register.

### Setup
```bash
# Using Django shell
python manage.py shell

>>> from core.models import Event, Trainee, EventRegistration
>>> from datetime import date, timedelta
>>> 
>>> # Create event with max 2 participants
>>> event = Event.objects.create(
...     name="Test Event - Max Participants",
...     event_date=date.today() + timedelta(days=10),
...     location="Test Location",
...     registration_deadline=date.today() + timedelta(days=5),
...     max_participants=2,
...     status='open'
... )
>>> 
>>> # Get 2 trainees
>>> trainees = Trainee.objects.all()[:2]
>>> print(f"Got {len(trainees)} trainees")
```

### Test Steps
1. Open trainee dashboard: http://127.0.0.1:8000/trainee/dashboard/
2. Find "Test Event - Max Participants" in the events list
3. Click "Register"
4. Confirm registration
5. Logout and login as different trainee
6. Find same event
7. Click "Register"
8. Confirm registration

### Expected Result
- ✅ First registration succeeds
- ✅ Event still shows as "Open" for first trainee
- ✅ Second registration succeeds
- ✅ Event immediately shows as "CLOSED" for both trainees
- ✅ Event status in database changes to 'closed'
- ✅ Notification about closure is created

### Verification
```bash
>>> event.refresh_from_db()
>>> print(f"Event status: {event.status}")  # Should be 'closed'
>>> print(f"Participants: {event.participant_count}/{event.max_participants}")
>>> 
>>> from core.models import Notification
>>> notifications = Notification.objects.filter(event=event)
>>> print(f"Created {notifications.count()} notifications")
>>> for n in notifications:
...     print(f"  - {n.title}: {n.message[:50]}")
```

---

## Test Case 3: Admin View Auto-Closure Detection

### Objective
Verify admin views detect and handle auto-closure conditions.

### Test 3A: Create Event with Past Deadline

**Setup:**
Use admin panel to create event

**Steps:**
1. Go to http://127.0.0.1:8000/admin/events/add/
2. Fill in form:
   - Event Name: "Test Create Event"
   - Event Date: Pick date 10 days from now
   - Registration Deadline: Pick date 1 day ago
   - Location: "Test Location"
   - Max Participants: "5"
   - Status: "Open for Registration"
3. Click "Create Event"

**Expected Result:**
- ✅ Warning message: "Event created but registration is already closed (deadline has passed)"
- ✅ Event is created with status='closed'

**Verification:**
```bash
>>> event = Event.objects.get(name="Test Create Event")
>>> print(f"Status: {event.status}")  # Should be 'closed'
```

### Test 3B: Edit Event to Set Past Deadline

**Steps:**
1. Go to http://127.0.0.1:8000/admin/events/
2. Find any event with status='open'
3. Click edit
4. Change registration deadline to yesterday
5. Click "Update Event"

**Expected Result:**
- ✅ Warning message about auto-closure
- ✅ Event status changes to 'closed'

---

## Test Case 4: Management Command

### Objective
Verify management command closes expired events.

### Setup
```bash
# Using Django shell
python manage.py shell

>>> from core.models import Event
>>> from datetime import date, timedelta
>>> 
>>> # Create 3 test events
>>> for i in range(3):
...     Event.objects.create(
...         name=f"Expired Event {i+1}",
...         event_date=date.today() + timedelta(days=10),
...         location=f"Location {i+1}",
...         registration_deadline=date.today() - timedelta(days=1),  # Expired
...         max_participants=10,
...         status='open'
...     )
>>> 
>>> open_events = Event.objects.filter(status='open')
>>> print(f"Open events before: {open_events.count()}")
```

### Test Steps
1. Run management command:
```bash
python manage.py close_expired_events
```

### Expected Result
```
Closed "Expired Event 1" - Registration deadline (2026-01-10) passed
Closed "Expired Event 2" - Registration deadline (2026-01-10) passed
Closed "Expired Event 3" - Registration deadline (2026-01-10) passed

Successfully closed 3 event(s)
```

### Verification
```bash
>>> from core.models import Event
>>> open_events = Event.objects.filter(status='open')
>>> print(f"Open events after: {open_events.count()}")  # Should be less
>>> 
>>> closed_events = Event.objects.filter(status='closed')
>>> print(f"Total closed: {closed_events.count()}")
```

---

## Test Case 5: Notification System

### Objective
Verify notifications are created and displayed.

### Setup
Perform Test Case 2 (Max Participants) first

### Test Steps
1. Open trainee notifications: http://127.0.0.1:8000/trainee/notifications/
2. Look for notification about event closure

### Expected Result
- ✅ Notification appears with title "Event Registration Closed: [Event Name]"
- ✅ Message includes reason: "Maximum participants (X) reached"
- ✅ Event date is included in message

### Verification
```bash
>>> from core.models import Notification, Event
>>> event = Event.objects.get(name="Test Event - Max Participants")
>>> notifications = Notification.objects.filter(event=event)
>>> 
>>> print(f"Total notifications: {notifications.count()}")
>>> for notif in notifications:
...     print(f"\nTitle: {notif.title}")
...     print(f"Message: {notif.message}")
...     print(f"Type: {notif.notification_type}")
```

---

## Test Case 6: Edge Cases

### Test 6A: Register When Event Already Closed

**Setup:**
- Create event and close it manually (set status='closed')
- Or wait for auto-closure via test case 2

**Steps:**
1. Try to register as trainee
2. Check if registration form is disabled/hidden

**Expected Result:**
- ✅ Registration button is disabled
- ✅ Message shows "Registration closed"

### Test 6B: Deadline on Today's Date

**Setup:**
```bash
python manage.py shell

>>> from core.models import Event
>>> from datetime import date
>>> 
>>> event = Event.objects.create(
...     name="Today Deadline Event",
...     event_date=date.today() + timedelta(days=5),
...     location="Test",
...     registration_deadline=date.today(),  # Today
...     max_participants=10,
...     status='open'
... )
```

**Test:**
```bash
python manage.py close_expired_events
```

**Expected Result:**
- ✅ Event is NOT closed (deadline hasn't passed yet, today is still valid)

### Test 6C: Very Large Participant Count

**Setup:**
Create event with max_participants=1000

**Steps:**
1. Register 999 trainees
2. Register 1000th trainee

**Expected Result:**
- ✅ Event closes after 1000th registration
- ✅ No performance degradation

---

## Test Case 7: Manual Re-Opening (if implemented)

**Note:** Current implementation doesn't prevent manual status change.

**Test Steps:**
1. Close event (via deadline or max)
2. Go to admin: edit event
3. Change status back to 'open'
4. Save

**Expected Result:**
- ✅ Admin can manually reopen event
- ⚠️ Note: New registrations would be accepted unless deadline has passed

---

## Regression Tests

### Test R1: Existing Event Functionality Still Works

**Steps:**
1. Create normal event (deadline in future, open status)
2. Register trainees normally
3. Verify event behaves as before

**Expected Result:**
- ✅ All existing functionality works
- ✅ No breaking changes

### Test R2: Trainee Can See Event Details

**Steps:**
1. Go to events page
2. Click on event details

**Expected Result:**
- ✅ Event information displays correctly
- ✅ Participant count shown accurately
- ✅ Registration button state reflects closure

### Test R3: Admin Dashboard Reports

**Steps:**
1. Go to admin dashboard
2. Check events section

**Expected Result:**
- ✅ Event counts accurate
- ✅ Status filters work
- ✅ No errors in console

---

## Performance Tests

### Test P1: Management Command Performance

```bash
# Create 100 events with expired deadlines
python manage.py shell

>>> from core.models import Event
>>> from datetime import date, timedelta
>>> 
>>> for i in range(100):
...     Event.objects.create(
...         name=f"Perf Test Event {i}",
...         event_date=date.today() + timedelta(days=10),
...         location="Test",
...         registration_deadline=date.today() - timedelta(days=1),
...         max_participants=10,
...         status='open'
...     )
```

**Test:**
```bash
time python manage.py close_expired_events
```

**Expected Result:**
- ✅ Command completes in under 30 seconds
- ✅ No database locks
- ✅ All 100 events closed

### Test P2: Registration Performance

**Steps:**
1. Create event with high max_participants (1000)
2. Register many trainees in sequence
3. Monitor response time

**Expected Result:**
- ✅ Registration response <500ms even with 999+ participants
- ✅ Signal processing doesn't cause slowdown

---

## Cleanup After Testing

```bash
# Delete test events
python manage.py shell

>>> from core.models import Event
>>> Event.objects.filter(name__startswith="Test").delete()
>>> Event.objects.filter(name__startswith="Expired").delete()
>>> Event.objects.filter(name__startswith="Perf").delete()
```

---

## Test Report Template

```
Date: ___________
Tester: ___________
Environment: Development / Staging / Production

Test Case 1 - Deadline-Based Auto-Closure
  Status: ☐ PASS ☐ FAIL ☐ SKIP
  Notes: ___________

Test Case 2 - Max Participants Auto-Closure
  Status: ☐ PASS ☐ FAIL ☐ SKIP
  Notes: ___________

Test Case 3 - Admin View Auto-Closure
  Status: ☐ PASS ☐ FAIL ☐ SKIP
  Notes: ___________

Test Case 4 - Management Command
  Status: ☐ PASS ☐ FAIL ☐ SKIP
  Notes: ___________

Test Case 5 - Notification System
  Status: ☐ PASS ☐ FAIL ☐ SKIP
  Notes: ___________

Test Case 6 - Edge Cases
  Status: ☐ PASS ☐ FAIL ☐ SKIP
  Notes: ___________

Test Case 7 - Manual Re-Opening
  Status: ☐ PASS ☐ FAIL ☐ SKIP
  Notes: ___________

Regression Tests
  Status: ☐ PASS ☐ FAIL ☐ SKIP
  Notes: ___________

Performance Tests
  Status: ☐ PASS ☐ FAIL ☐ SKIP
  Notes: ___________

Overall Result: ☐ PASS ☐ FAIL ☐ CONDITIONAL
Comments: ___________
```

---

## Troubleshooting

### Events not closing automatically?
- Check event status is 'open'
- Verify registration_deadline is in the past
- Run management command manually: `python manage.py close_expired_events`
- Check Django logs for errors

### Signals not firing?
- Verify signals module is imported in `core/__init__.py`
- Check Django apps are configured
- Look for import errors in console

### Notifications not showing?
- Verify trainees exist and status='active'
- Check Notification model in database
- Review admin notifications interface

### Management command doesn't find events?
- Check Event.objects.filter(status='open').count() in shell
- Verify database connection
- Check for filtering issues in query


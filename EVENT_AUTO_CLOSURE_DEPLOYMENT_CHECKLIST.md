# Event Auto-Closure Feature - Deployment Checklist

## Pre-Deployment Review

### Code Review
- [ ] Review `core/models.py` changes
  - [ ] `should_close()` method implemented correctly
  - [ ] `close_registration()` method implemented correctly
  - [ ] Methods use proper date comparisons
  - [ ] No SQL injection vulnerabilities
  - [ ] Error handling in place

- [ ] Review `core/signals.py` changes
  - [ ] Signal imports are correct
  - [ ] `auto_close_event_on_registration` only triggers on creation
  - [ ] Notification service is called correctly
  - [ ] Exception handling for signal failures

- [ ] Review `core/views/admin.py` changes
  - [ ] Both event_add and event_edit call closure check
  - [ ] Warning messages are user-friendly
  - [ ] No breaking changes to form validation
  - [ ] User feedback is clear

- [ ] Review `core/services/notification_service.py` changes
  - [ ] `create_event_closed_notification()` handles both closure reasons
  - [ ] Bulk create for efficiency
  - [ ] Proper message formatting

- [ ] Review `core/management/commands/close_expired_events.py`
  - [ ] Command syntax is correct
  - [ ] Error handling for database failures
  - [ ] Proper logging/output
  - [ ] Can be run safely multiple times

## Testing Verification

### Unit Tests
- [ ] Models - `should_close()` returns correct values
- [ ] Models - `close_registration()` updates status
- [ ] Signals - Auto-close on registration
- [ ] Views - Admin checks closure conditions
- [ ] Management command - Closes expired events
- [ ] Notifications - Created with correct message

### Integration Tests
- [ ] End-to-end registration closure
- [ ] End-to-end deadline closure
- [ ] Admin interface behavior
- [ ] Notification delivery
- [ ] Database state consistency

### Manual Testing (see TEST_GUIDE.md)
- [ ] Test Case 1 - Deadline closure
- [ ] Test Case 2 - Max participants closure
- [ ] Test Case 3 - Admin view detection
- [ ] Test Case 4 - Management command
- [ ] Test Case 5 - Notifications
- [ ] Test Case 6 - Edge cases
- [ ] Edge Case Tests completed
- [ ] Regression tests passed

### Performance Testing
- [ ] Signal doesn't slow down registration
- [ ] Management command completes in reasonable time
- [ ] No database locks
- [ ] Bulk notifications efficient
- [ ] Load tested with 100+ events

## Documentation Review

- [ ] `EVENT_AUTO_CLOSURE_IMPLEMENTATION.md` - Complete and accurate
- [ ] `EVENT_AUTO_CLOSURE_QUICK_REFERENCE.md` - Clear and helpful
- [ ] `EVENT_AUTO_CLOSURE_FLOW_DIAGRAM.md` - Accurate diagrams
- [ ] `EVENT_AUTO_CLOSURE_TEST_GUIDE.md` - Comprehensive test cases
- [ ] Code comments are clear
- [ ] Docstrings are complete

## Production Preparation

### Database
- [ ] No migrations needed (confirmed)
- [ ] Existing data compatible
- [ ] No schema changes required
- [ ] Backup taken before deployment

### Configuration
- [ ] Settings are correct
- [ ] Debug mode appropriate for environment
- [ ] Logging configured
- [ ] Error reporting configured

### Scheduling
- [ ] Cron job configured for management command
  - [ ] Correct path to Python/manage.py
  - [ ] Correct working directory
  - [ ] Correct environment variables
  - [ ] Cron log location configured
  - [ ] Executed at appropriate time (1 AM recommended)

- [ ] Alternative: Task scheduler configured (if Windows)
  - [ ] Task runs with correct user
  - [ ] Error handling configured
  - [ ] Log file location set

### Monitoring
- [ ] Logging configured for signal handlers
- [ ] Logging configured for management command
- [ ] Error alerts configured
- [ ] Monitoring for task execution

## Deployment Steps

### Step 1: Pre-Deployment
```bash
# On development/staging
- [ ] Run all tests
- [ ] Verify no conflicts with existing code
- [ ] Backup database
- [ ] Document any custom configurations
```

### Step 2: Code Deployment
```bash
# Pull latest code
- [ ] git pull origin main

# Verify files
- [ ] Confirm all 5 modified files are updated
- [ ] Confirm 3 new files are present
- [ ] Confirm 2 documentation files added

# No migrations needed
- [ ] Confirmed: no new models
- [ ] Confirmed: no field changes
- [ ] Confirmed: no schema changes
```

### Step 3: Service Restart (if needed)
```bash
- [ ] Stop web service
- [ ] Verify processes stopped
- [ ] Start web service
- [ ] Verify service health
- [ ] Check logs for errors
```

### Step 4: Cron Job Configuration
```bash
# As root or appropriate user
crontab -e

# Add this line (for 1 AM daily execution):
0 1 * * * cd /path/to/karate && /path/to/venv/bin/python manage.py close_expired_events >> /var/log/karate/close_events.log 2>&1

# Or using helper script:
0 1 * * * cd /path/to/karate && python run_close_expired_events.py >> /var/log/karate/close_events.log 2>&1

- [ ] Cron entry added
- [ ] Syntax verified: `crontab -l`
- [ ] Log directory exists: `mkdir -p /var/log/karate`
- [ ] Log file writable
```

### Step 5: Verification
```bash
# Test management command manually
python manage.py close_expired_events

# Verify:
- [ ] No errors in output
- [ ] Shows "Successfully closed X event(s)"
- [ ] Correct events are closed
- [ ] Notifications created

# Check database
python manage.py shell
>>> from core.models import Event
>>> closed = Event.objects.filter(status='closed')
>>> print(f"Closed events: {closed.count()}")
```

### Step 6: Smoke Tests
- [ ] Admin can create event (no errors)
- [ ] Admin can edit event (no errors)
- [ ] Trainee can see events (no errors)
- [ ] Trainee can register (no errors)
- [ ] Events close properly on registration
- [ ] Notifications appear (no errors)

## Post-Deployment

### Day 1
- [ ] Monitor application logs
- [ ] Check for any errors
- [ ] Verify event status updates working
- [ ] Check signal execution in logs
- [ ] Confirm notifications appearing

### Day 2-7
- [ ] Continue monitoring logs
- [ ] Test manual closure still works
- [ ] Verify cron job executed (check logs)
- [ ] Validate performance (response times)
- [ ] Check database for issues

### Week 1-2
- [ ] Review cron job execution logs
- [ ] Verify all closed events accurate
- [ ] Check trainee experience
- [ ] Performance baseline established
- [ ] No reported issues

## Rollback Plan

If issues occur:

### Quick Rollback
```bash
# Option 1: Disable signals (temporary)
Edit core/signals.py:
Comment out @receiver(post_save, sender=EventRegistration)
Comment out auto_close_event_on_registration function

# Option 2: Disable management command
Remove cron job entry
crontab -e
# Delete the line calling close_expired_events
```

### Full Rollback
```bash
# Revert code to previous version
git revert <commit_hash>

# Or checkout previous version
git checkout HEAD~1 -- core/models.py
git checkout HEAD~1 -- core/signals.py
git checkout HEAD~1 -- core/views/admin.py
git checkout HEAD~1 -- core/services/notification_service.py

# Restart service
systemctl restart karate  # or appropriate command
```

### Data Recovery
- [ ] Closed events can be manually reopened
- [ ] Notifications can be deleted
- [ ] No data loss possible
- [ ] Database rollback available if needed

## Sign-Off

- [ ] **Developer**: _____________ Date: _______
  - Confirms: Code reviewed, tested, ready for deployment

- [ ] **QA/Tester**: _____________ Date: _______
  - Confirms: All tests passed, no issues found

- [ ] **DevOps/Deployment**: _____________ Date: _______
  - Confirms: Environment prepared, deployment ready

- [ ] **Product Owner**: _____________ Date: _______
  - Confirms: Feature meets requirements, approved for release

## Monitoring Checklist (Post-Deployment)

### Daily Checks
```bash
# Check cron execution
tail -f /var/log/karate/close_events.log

# Check Django logs
tail -f /var/log/django.log

# Check for errors
grep -i error /var/log/karate/close_events.log
grep -i error /var/log/django.log
```

### Weekly Checks
- [ ] Review event status distribution
- [ ] Check notification creation rate
- [ ] Verify no false closures
- [ ] Performance metrics stable
- [ ] No user complaints

### Monthly Checks
- [ ] Full test cycle
- [ ] Database optimization
- [ ] Log file rotation
- [ ] Documentation updates
- [ ] Performance analysis

## Support Contacts

- **Development Team**: _____________ Phone: _______
- **DevOps Team**: _____________ Phone: _______
- **On-Call Support**: _____________ Phone: _______

## Additional Notes

```
_____________________________________________________________________________
_____________________________________________________________________________
_____________________________________________________________________________
_____________________________________________________________________________
```

---

## Quick Command Reference

### View Cron Jobs
```bash
crontab -l
```

### Test Cron Command
```bash
# Run manually at any time
python manage.py close_expired_events

# Or with helper script
python run_close_expired_events.py
```

### Check Event Status
```bash
python manage.py shell
>>> from core.models import Event
>>> Event.objects.values('status').annotate(count=Count('id'))
```

### Monitor Logs
```bash
# Real-time monitoring
tail -f /var/log/karate/close_events.log

# Search for errors
grep -i "error\|closed\|failed" /var/log/karate/close_events.log

# Last 100 lines
tail -n 100 /var/log/karate/close_events.log
```

### Emergency Disable
```bash
# Quick disable (remove cron)
crontab -e
# Delete the line with close_expired_events

# Or disable in code
# Edit core/signals.py, comment out the signal handler
```

---

**Checklist Version:** 1.0  
**Last Updated:** January 11, 2026  
**Status:** Ready for Deployment

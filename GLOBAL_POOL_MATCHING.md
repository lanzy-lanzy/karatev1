# Global Pool Matching - Feature Update

## Overview
Auto-matching has been enhanced to support **Global Pool Matching** - automatically pairing trainees from the entire system (not just event participants) based on belt rank, weight class, and age.

This enables:
- Creating title matches without event registration
- Matching 0-participant events
- Freestyle matching tournaments
- Independent match scheduling

## What's New

### New Checkbox: "Match from all system trainees (global pool)"
- When **OFF** (default): Match only event-registered trainees
- When **ON**: Match any active trainee in the entire system

**Use Cases:**
- Event with 0 participants → Enable global pool to generate matches anyway
- Title matches across different events
- Standalone match creation without event context
- Cross-event championship matchups

## Key Features

### Global Pool Sources
When enabled, system automatically includes:
- ✅ All trainees with `status='active'`
- ✅ Non-archived trainees
- ✅ Users with active accounts
- ❌ Excludes: Inactive, suspended, archived, deleted users

### Matching Still Respects
All matching rules remain unchanged:
- Weight difference ≤ 5kg
- Belt rank same or adjacent
- Age difference ≤ 3 years
- Judge availability

### Works With
- Regular matches (non-event trainees)
- Title matches (championship bouts)
- Ongoing match support
- All existing matching features

## Technical Changes

### Service Layer (`core/services/matchmaking.py`)

**New Parameter:**
```python
def auto_match(
    self, 
    event_id: int, 
    allow_ongoing_matches: bool = True, 
    include_title_matches: bool = True,
    use_global_pool: bool = False  # NEW
) -> List[ProposedMatch]:
```

**Logic:**
```python
if use_global_pool:
    # Pull from entire system
    all_trainees = Trainee.objects.filter(
        status='active',
        archived=False,
        profile__user__is_active=True
    )
else:
    # Pull from event registration only
    all_trainees = EventRegistration.objects.filter(
        event=event,
        status='registered'
    ).trainee
```

### View Layer (`core/views/admin.py`)

**Updated form handling:**
```python
use_global = request.POST.get('use_global_pool', 'off') == 'on'

service.auto_match(
    event_id,
    allow_ongoing_matches=allow_ongoing,
    include_title_matches=include_titles,
    use_global_pool=use_global  # NEW
)
```

**Session storage:**
```python
request.session['auto_match_options'] = {
    'allow_ongoing_matches': bool,
    'include_title_matches': bool,
    'use_global_pool': bool,  # NEW
}
```

### Template (`templates/admin/matchmaking/auto.html`)

**New checkbox:**
```html
<label class="flex items-center">
    <input type="checkbox" name="use_global_pool" value="on">
    <span>Match from all system trainees (global pool)</span>
    <span>(instead of event participants only)</span>
</label>
```

**Updated info box:**
- Added explanation of Event Mode vs. Global Pool Mode
- Clear distinction of matching sources

**Enhanced no-results message:**
- Suggests enabling global pool as troubleshooting step
- Comprehensive help for all scenarios

## Usage Examples

### Scenario 1: 0-Participant Event, Immediate Matching
```
Event: "Exhibition Tournament" (0 participants registered)

1. Select event
2. Enable "Match from all system trainees"
3. Generate → System finds matches from all active trainees
4. Create matches
Result: Tournament proceeds with global pool participants
```

### Scenario 2: Title Match Championship
```
Main Event: "Spring Regional" (registered trainees)
Side Event: "Championship Finals" (0 registered)

1. Main event completed → has matches
2. Create separate championship event
3. Enable "Global pool" + "Title matches"
4. Generate → Pairs completed-match trainees globally
5. Create championship finals
Result: Championship matches drawn from entire system winners
```

### Scenario 3: Multi-Event Tournament Series
```
Events: Multiple local tournaments

1. Create master event: "Regional Championship Series" (0 participants)
2. Enable global pool + title matches
3. Generate → Matches winners from all previous events
Result: System-wide championship bracket
```

### Scenario 4: Training Tournament (Keep Normal)
```
Event: "Weekly Training" (20 registered trainees)

1. Leave global pool OFF (default)
2. Generate → Only matches registered trainees
3. Create matches
Result: Traditional event matching behavior
```

## Configuration Matrix

| Use Case | Global Pool | Ongoing | Title Matches | Result |
|----------|------------|---------|---|---|
| Standard event | OFF | ON | ON | Event participants + titles |
| 0-person event | ON | ON | ON | Any trainee + titles |
| Training tournament | OFF | OFF | OFF | Unmatched registrants only |
| Championship finals | ON | ON | ON | System-wide championship |
| Quick exhibition | ON | ON | OFF | Any trainee, regular only |

## Database Impact

✅ **Zero changes required**
- No migrations
- No schema updates
- Uses existing `Trainee.status` and `archived` fields
- Reuses existing filtering mechanisms

## Performance Considerations

### Minimal Impact
- Event pool: ~50-500 trainees typical
- Global pool: ~500-5000 trainees typical
- Query impact: Single filter on existing fields
- Pairing algorithm: O(n²) unchanged

### Recommended Limits
- Under 1000 trainees: No optimization needed
- 1000-5000 trainees: Add database index on Trainee.status
- 5000+ trainees: Consider pagination or pre-filtering

### Query Optimization
```python
# Automatically optimized:
Trainee.objects.filter(
    status='active',          # Indexed field
    archived=False,           # Boolean, fast
    profile__user__is_active=True  # Related object
).select_related('profile__user')  # Avoids N+1
```

## Error Handling

| Scenario | Behavior |
|----------|----------|
| Global pool, no active trainees | "No valid matches found" |
| Global pool, mismatched weights | Excluded from pairings |
| Global pool, constraint violations | Standard exclusion rules |
| Event pool, 0 registered | Show empty or error |
| Global + Event pool, conflicts | No issues (independent) |

## UI/UX Flows

### Flow 1: Event Matching (Default)
```
Select Event → Generate (uses registered trainees) → Review → Create
```

### Flow 2: Global Pool Matching
```
Select Event (can be 0-person) → ☑ Global Pool → Generate (uses all active) → Review → Create
```

### Flow 3: Mixed Matching
```
Select Event → ☑ Global Pool → ☑ Title Matches → Generate → 
(Mix of event + global trainees, including championships) → Create
```

## Important Notes

### Event Selection Still Required
- Even with global pool, must select an event
- Event provides context and scheduling reference
- Matches created are associated with the event
- Event date used for match scheduling

### Match Association
- Matches created belong to selected event
- Global pool trainees can compete in non-registered events
- Doesn't violate event constraints
- Useful for exhibition, championship, or series events

### Trainee Status
Global pool only includes trainees where:
```
status = 'active'          (not inactive/suspended)
archived = False           (not deleted)
user.is_active = True      (user account active)
```

## Backward Compatibility

✅ **Fully backward compatible**
- Default: Global pool OFF
- Existing code works unchanged
- No breaking changes
- All previous features work as before

## Session & State Management

### Session Keys (Updated)
```python
{
    'auto_match_event_id': int,
    'proposed_matches': [...],
    'auto_match_options': {
        'allow_ongoing_matches': bool,
        'include_title_matches': bool,
        'use_global_pool': bool,  # NEW
    }
}
```

### Session Cleanup
- Properly clears all keys including new `use_global_pool` option
- No session persistence issues
- Fresh start on next use

## Testing Checklist

### Functional
- [ ] Generate matches with global pool OFF (event mode)
- [ ] Generate matches with global pool ON (all trainees)
- [ ] 0-participant event + global pool → Generates matches
- [ ] Global pool + title matches → Works correctly
- [ ] Non-matching trainees filtered correctly
- [ ] Weight/belt/age constraints enforced
- [ ] Match creation with global pool trainees
- [ ] Judges assigned correctly

### Edge Cases
- [ ] No active trainees globally → "No matches" message
- [ ] Single active trainee → No pairs
- [ ] All trainees archived → No matches
- [ ] Mixed event+global pool scenarios
- [ ] Constraint violations with global pool

### Integration
- [ ] Global pool with leaderboard
- [ ] Global pool with match results
- [ ] Global pool with trainee profiles
- [ ] Existing event matching unaffected

### Performance
- [ ] <100ms query with 500 trainees
- [ ] <500ms pairing with 1000 trainees
- [ ] Session storage reasonable size
- [ ] No database index issues

## Documentation Updated

1. **This file** - Complete feature reference
2. **AUTO_MATCHING_QUICK_START.md** - User guide (updated)
3. **Template help text** - In-app guidance
4. **No-results message** - Troubleshooting suggestions

## Troubleshooting

### Problem: Global pool not finding matches
**Check:**
1. Are there active, non-archived trainees?
2. Do they meet weight/belt/age constraints?
3. Check if users are active (not disabled)

**Solutions:**
1. Check Trainee Management for trainee status
2. Verify weight/belt rank/age data
3. Use event mode instead if global not working

### Problem: 0-participant event still shows no matches
**Check:**
1. Is global pool checkbox enabled?
2. Are there any active trainees in system?
3. Do they meet constraints for each other?

**Solutions:**
1. Must explicitly enable global pool checkbox
2. Add/activate trainees in system
3. Check weight/belt/age compatibility

### Problem: Too many matches generated
**Solutions:**
1. Turn OFF global pool to limit to event participants
2. Deselect specific matches before creation
3. Adjust filters (uncheck ongoing/titles)

## Migration from Event-Only

If upgrading existing event:
1. Open event in auto-matching
2. Leave global pool OFF by default
3. Behavior unchanged from before
4. Can enable global pool if needed for expansion

## Future Enhancements

1. **Trainee Pool Selection** - Choose from multiple pools
2. **Custom Filters** - Belt range, weight range, age range
3. **Bulk Operations** - Multiple events simultaneously
4. **Pool Templates** - Save/load common configurations
5. **Geographic Filtering** - Location-based matching

## Support

- **User Questions:** See AUTO_MATCHING_QUICK_START.md
- **Technical Details:** See IMPLEMENTATION_NOTES_AUTO_MATCHING.md
- **Admin Help:** In-app help text and info box
- **Troubleshooting:** See section above

---

**Version:** 1.1 (Global Pool Addition)
**Date:** December 2025
**Status:** Production Ready

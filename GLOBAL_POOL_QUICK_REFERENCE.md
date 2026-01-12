# Global Pool Matching - Quick Reference

## The Problem You Solved
**Before:** Auto-matching only worked with event-registered trainees
**Now:** Can create matches from ANY active trainee in the system (ignores event registration)

## When to Use Global Pool

### ✅ USE Global Pool When:
- Event has **0 registered participants** but you want to create matches anyway
- Creating **title/championship matches** across the entire system
- Running a **standalone tournament** not tied to event registration
- Need to **match unregistered trainees** for an event
- Want **system-wide championship finals**

### ❌ DON'T Use Global Pool When:
- Only want to match **registered event participants**
- Running a **standard tournament** with registration
- Need to exclude non-registered trainees
- Require event registration validation

## How It Works

### Step-by-Step

1. **Go to Auto-Matchmaking**
   Admin → Matchmaking → Auto-Matchmaking

2. **Select Event**
   (Even if 0 participants - event still needed for scheduling)

3. **Check "Match from all system trainees"**
   ☑ Match from all system trainees (global pool)

4. **Generate Matches**
   System searches ALL active trainees (not just registered)

5. **Create Matches**
   Selected matches created with chosen judges

## Configuration Options

### Three New Toggles:

| Option | Purpose | Default |
|--------|---------|---------|
| **Global Pool** | Match from all system trainees | OFF |
| **Ongoing Matches** | Allow trainees with scheduled matches | ON |
| **Title Matches** | Include championship bouts | ON |

### Recommended Combinations:

```
Use Case 1: Normal Tournament
☑ Ongoing: ON  |  ☑ Title: ON  |  ☐ Global: OFF
Result: Event participants + title matches

Use Case 2: 0-Person Event
☑ Ongoing: ON  |  ☑ Title: ON  |  ☑ Global: ON
Result: Any trainee in system + title matches

Use Case 3: Championship Finals
☑ Ongoing: ON  |  ☑ Title: ON  |  ☑ Global: ON
Result: System-wide championship bracket

Use Case 4: Simple Training
☐ Ongoing: OFF |  ☐ Title: OFF |  ☐ Global: OFF
Result: Only unmatched event registrants
```

## What Changes

### Files Modified
1. `core/services/matchmaking.py` - Added `use_global_pool` parameter
2. `core/views/admin.py` - Reads global pool checkbox, passes to service
3. `templates/admin/matchmaking/auto.html` - Added checkbox + help text

### What Stays the Same
- All matching constraints (weight, belt, age)
- Judge requirements
- Match creation process
- Event association
- Everything else works as before

## Examples

### Example 1: 0-Participant Event
```
Event: "Quick Exhibition"
Registered: 0 trainees

Step 1: Select event
Step 2: ☑ Global pool
Step 3: Generate → Finds matches from all 800 system trainees
Step 4: Create matches
Result: Exhibition happens with global participants
```

### Example 2: Championship Tournament
```
Events: Spring Regional (20 participants) completed

Now want to create: Championship Finals (0 registered)

Step 1: Create new "Championship Finals" event
Step 2: Select it
Step 3: ☑ Global pool + ☑ Title matches
Step 4: Generate → System finds winners from regional
Step 5: Create → Championship matches created
Result: Championship finals with system-wide winners
```

### Example 3: Standard Event (Unchanged)
```
Event: "Monthly Training" (15 registered)

Step 1: Select event
Step 2: Leave ☐ Global pool unchecked
Step 3: Generate → Only 15 registered trainees matched
Step 4: Create → Normal tournament
Result: Same as before - only registered trainees
```

## Key Points

### ⭐ Important
1. **Event still required** - Use any event, even with 0 participants
2. **Event scheduling** - Matched trainees will compete in selected event
3. **Trainees must be active** - Only `status='active'` trainees included
4. **All constraints apply** - Weight/belt/age rules still enforced
5. **Combines with other options** - Works with ongoing + title matches

### ✅ Includes in Global Pool
- All trainees with status = 'Active'
- Non-archived trainees
- With active user accounts

### ❌ Excludes from Global Pool
- Inactive trainees
- Suspended trainees
- Archived/deleted trainees
- Disabled user accounts

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No matches found | ✓ Enable global pool ✓ Check trainee count ✓ Check constraints |
| Wrong trainees included | ✓ Check trainee status (active/inactive) ✓ Leave global off |
| Too many matches | ✓ Turn off title matches ✓ Deselect some ✓ Disable global pool |
| Event still needed | ✓ Always select event (for scheduling) |

## Performance

✅ **No issues** with:
- <1000 trainees
- <500 global matches
- Typical system loads

⚠️ **Consider optimization** with:
- >5000 trainees
- Frequent global matching
- Real-time requests

## Backward Compatibility

✅ **Fully compatible**
- Default: Global pool OFF
- Existing behavior unchanged
- All old matches still work
- No data loss

## Files to Read

| Document | For |
|----------|-----|
| `GLOBAL_POOL_MATCHING.md` | Complete technical reference |
| `AUTO_MATCHING_QUICK_START.md` | User guide |
| `IMPLEMENTATION_NOTES_AUTO_MATCHING.md` | Code details |
| This file | Quick reference |

## Quick Commands

### To Enable Global Pool Matching:
1. Admin Dashboard
2. Matchmaking → Auto-Matchmaking
3. Select any event
4. ☑ Check "Match from all system trainees"
5. Click "Generate Matches"
6. Review and create

### To Use Without Global Pool (Normal):
1. Admin Dashboard
2. Matchmaking → Auto-Matchmaking
3. Select event with registered trainees
4. ☐ Leave "Match from all..." unchecked
5. Click "Generate Matches"
6. Review and create

## Summary

| Aspect | Details |
|--------|---------|
| **What** | Match trainees from entire system, not just event |
| **When** | 0-person events, championships, exhibitions |
| **How** | Check one checkbox in auto-matching form |
| **Effect** | Auto-matching searches all active trainees globally |
| **Safety** | All constraints still applied |
| **Backward** | Fully compatible, default OFF |
| **Performance** | Negligible impact for typical systems |

---

**Last Updated:** December 2025
**Status:** Production Ready ✅

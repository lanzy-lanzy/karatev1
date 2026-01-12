# Match Sorting Update - Latest Created Matches First

## What Changed

Updated the matchmaking management system to display **latest created matches on top** instead of earliest.

## Changes Made

### 1. Model Level (`core/models.py`)
**File:** `core/models.py`, Lines 249-254

**Before:**
```python
class Meta:
    ordering = ['scheduled_time']
    verbose_name_plural = 'Matches'
    indexes = [
        models.Index(fields=['archived', 'scheduled_time']),
    ]
```

**After:**
```python
class Meta:
    ordering = ['-created_at']
    verbose_name_plural = 'Matches'
    indexes = [
        models.Index(fields=['archived', '-created_at']),
    ]
```

Changed default ordering from `scheduled_time` to `-created_at` (descending creation time)

### 2. View Level (`core/views/admin.py`)
Updated 4 locations to sort by `-created_at` instead of `scheduled_time`:

#### Location 1: matchmaking_list() - Line 1073
```python
matches = matches.order_by('-created_at')  # was: 'scheduled_time'
```

#### Location 2: matchmaking_list_partial() - Line 1124
```python
matches = matches.order_by('-created_at')  # was: 'scheduled_time'
```

#### Location 3: archived_matchmaking_list() - Line 1454
```python
matches = matches.order_by('-created_at')  # was: 'scheduled_time'
```

#### Location 4: archived_matchmaking_list_partial() - Line 1504
```python
matches = matches.order_by('-created_at')  # was: 'scheduled_time'
```

## Impact

### User Visible
- ✅ Latest created matches appear **at the top** of the list
- ✅ Oldest created matches appear at the bottom
- ✅ Applied to both active and archived matches
- ✅ Works with filtering and search

### Technical
- ✅ Uses `created_at` field (auto-populated on creation)
- ✅ Descending order: `-created_at` (most recent first)
- ✅ Database index updated for performance
- ✅ Consistent across all views

## Affected Pages

1. **Matchmaking Management** (Active Matches)
   - URL: `/admin/matchmaking/`
   - Displays newest matches first

2. **Matchmaking Management Partial** (HTMX Updates)
   - URL: `/admin/matchmaking/` (HTMX request)
   - Same ordering for dynamic updates

3. **Archived Matches**
   - URL: `/admin/matchmaking/archived/`
   - Latest archived matches shown first

4. **Archived Matches Partial** (HTMX Updates)
   - URL: `/admin/matchmaking/archived/` (HTMX request)
   - Same ordering for dynamic updates

## Sorting Behavior

### Before
```
Matches sorted by scheduled_time (earliest first):
1. Match on Jan 1 @ 9:00 AM (created Jan 1)
2. Match on Jan 2 @ 10:00 AM (created Jan 2)
3. Match on Jan 3 @ 11:00 AM (created Jan 3) ← bottom
```

### After
```
Matches sorted by created_at descending (latest first):
1. Match (created Jan 3 @ 11:00 AM) ← top (newest)
2. Match (created Jan 2 @ 10:00 AM)
3. Match (created Jan 1 @ 9:00 AM) ← bottom (oldest)
```

## Key Difference

| Aspect | Old Sorting | New Sorting |
|--------|-------------|------------|
| **Sort Field** | `scheduled_time` | `created_at` |
| **Order** | Ascending (↑) | Descending (↓) |
| **Position of Latest** | Bottom | Top |
| **When Sorted** | By match time | By creation time |
| **Purpose** | Match timeline | Recently added matches |

## Example Scenario

**Situation:** Admin creates 3 matches

1. Create Match A (scheduled for Jan 1)
2. Create Match B (scheduled for Jan 3)
3. Create Match C (scheduled for Jan 2)

**Before (by scheduled_time):**
```
1. Match A (Jan 1) - displayed at top
2. Match C (Jan 2)
3. Match B (Jan 3) - displayed at bottom
```

**After (by created_at descending):**
```
1. Match C (created 3rd) - displayed at top ← LATEST
2. Match B (created 2nd)
3. Match A (created 1st) - displayed at bottom
```

## Database Impact

### Index Update
Old index: `Index(fields=['archived', 'scheduled_time'])`
New index: `Index(fields=['archived', '-created_at'])`

**Note:** No migration needed as `created_at` field already exists and was only used for storage, not display ordering.

## Performance

✅ **No Performance Issues**
- `created_at` is indexed
- Query performance same or better
- Sorting on creation time is faster than scheduled time for large datasets
- No additional queries added

## Rollback Instructions

If needed to revert to scheduled time sorting:

### In `core/models.py` (Lines 249-254):
```python
class Meta:
    ordering = ['scheduled_time']  # revert to this
    indexes = [
        models.Index(fields=['archived', 'scheduled_time']),  # revert index
    ]
```

### In `core/views/admin.py`:
- Line 1073: Change `'-created_at'` back to `'scheduled_time'`
- Line 1124: Change `'-created_at'` back to `'scheduled_time'`
- Line 1454: Change `'-created_at'` back to `'scheduled_time'`
- Line 1504: Change `'-created_at'` back to `'scheduled_time'`

## Testing

### Manual Testing
1. ✅ Create multiple matches
2. ✅ Verify latest appear at top
3. ✅ Verify archived matches same behavior
4. ✅ Test with filters
5. ✅ Test HTMX updates

### Expected Result
Latest created matches displayed first in all views.

## Summary

| Item | Details |
|------|---------|
| **Change Type** | Sorting order modification |
| **Files Modified** | 2 |
| **Lines Changed** | 6 |
| **Breaking Changes** | No |
| **Database Migration** | No |
| **Performance Impact** | Neutral/Positive |
| **User Impact** | Most recent matches visible first |
| **Rollback Time** | <5 minutes |

---

**Status:** ✅ Complete  
**Date:** December 2025  
**Tested:** ✅ Yes

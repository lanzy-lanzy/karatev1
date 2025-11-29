# Implementation Details - Minimum Judges per Match

## Files Modified

### 1. `core/services/matchmaking.py`

**Added constant:**
```python
class MatchmakingService:
    MAX_WEIGHT_DIFF = Decimal('5.0')  # kg
    MAX_AGE_DIFF = 3  # years
    MIN_JUDGES_REQUIRED = 3  # Minimum judges per match (NEW)
```

**Updated assign_judges method:**
```python
def assign_judges(self, match_id: int, judge_ids: List[int]) -> bool:
    match = Match.objects.get(id=match_id)
    event = match.event
    
    # NEW: Validate minimum number of judges
    if len(judge_ids) < self.MIN_JUDGES_REQUIRED:
        return False
    
    # Validate each judge for conflicts
    for judge_id in judge_ids:
        if not self.validate_judge_assignment(judge_id, event.id):
            return False
    
    # Assign judges to match
    match.judge_assignments.all().delete()
    for judge_id in judge_ids:
        MatchJudge.objects.create(match=match, judge_id=judge_id)
    
    return True
```

### 2. `core/views/admin.py`

**In match_add() view:**
```python
# BEFORE: No judge validation
if not scheduled_time:
    errors['scheduled_time'] = 'Scheduled time is required'

# AFTER: Added judge count validation
if not scheduled_time:
    errors['scheduled_time'] = 'Scheduled time is required'
if len([j for j in judge_ids if j]) < 3:  # NEW
    errors['judges'] = 'At least 3 judges must be selected'  # NEW

# Also updated form_data to include judge errors:
'judges': {'value': judge_ids, 'errors': [errors.get('judges')] if errors.get('judges') else []},
```

**In match_edit() view:**
```python
# Same validation added as in match_add()
if len([j for j in judge_ids if j]) < 3:
    errors['judges'] = 'At least 3 judges must be selected'

# Form data updated to show errors
'judges': {'value': judge_ids, 'errors': [errors.get('judges')] if errors.get('judges') else []},
```

**In auto_matchmaking() view:**
```python
# BEFORE: Only passed events
context = {
    'events': events,
    'proposed_matches': proposed_matches,
    'selected_event': selected_event,
}

# AFTER: Added judges for selection
judges = Judge.objects.filter(is_active=True).select_related('profile__user')  # NEW
context = {
    'events': events,
    'judges': judges,  # NEW
    'proposed_matches': proposed_matches,
    'selected_event': selected_event,
}
```

**In auto_matchmaking_confirm() view:**
```python
# BEFORE: No judge selection in auto-match
match = Match.objects.create(
    event_id=event_id,
    competitor1_id=pm['competitor1_id'],
    competitor2_id=pm['competitor2_id'],
    scheduled_time=scheduled_time
)

# AFTER: Added judge validation and assignment
judge_ids = request.POST.getlist('judges')  # NEW
valid_judge_ids = [j for j in judge_ids if j]  # NEW
if len(valid_judge_ids) < 3:  # NEW
    messages.error(request, 'At least 3 judges must be selected for auto-matched games.')  # NEW
    return redirect('admin_auto_matchmaking')  # NEW

# ... later in loop ...
match = Match.objects.create(...)  # Same as before

# NEW: Assign judges to the match
for judge_id in valid_judge_ids:
    MatchJudge.objects.create(match=match, judge_id=judge_id)

# Updated success message
messages.success(request, f'{created_count} matches have been created successfully with {len(valid_judge_ids)} judges assigned.')
```

### 3. `templates/admin/matchmaking/form.html`

**Before:**
```html
<!-- Judges -->
<div>
    <label class="block text-sm font-medium text-gray-700 mb-1">Assign Judges</label>
    <div class="space-y-2 max-h-48 overflow-y-auto border border-gray-300 rounded-lg p-3">
        <!-- checkboxes -->
    </div>
</div>
```

**After:**
```html
<!-- Judges -->
<div>
    <label class="block text-sm font-medium text-gray-700 mb-1">
        Assign Judges <span class="text-red-600">*</span> (Minimum 3)
    </label>
    <div class="space-y-2 max-h-48 overflow-y-auto border {% if form.judges.errors %}border-red-500{% else %}border-gray-300{% endif %} rounded-lg p-3">
        <!-- checkboxes -->
    </div>
    {% if form.judges.errors %}
    <p class="mt-1 text-sm text-red-600">{{ form.judges.errors.0 }}</p>
    {% else %}
    <p class="mt-1 text-xs text-gray-500">Select at least 3 judges to officiate this match</p>
    {% endif %}
</div>
```

Changes:
- Added required indicator (*)
- Added "(Minimum 3)" note
- Changed border color on error
- Show error message if validation fails
- Show helpful hint text otherwise

### 4. `templates/admin/matchmaking/auto.html`

**Before:**
```html
<div class="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
    <div>
        <h3 class="text-lg font-medium text-gray-900">Proposed Matches for {{ selected_event.name }}</h3>
        <p class="text-sm text-gray-500 mt-1">{{ proposed_matches|length }} matches generated</p>
    </div>
    <button type="submit" ...>Create Selected Matches</button>
</div>
```

**After:**
```html
<div class="px-6 py-4 border-b border-gray-200">
    <h3 class="text-lg font-medium text-gray-900">Proposed Matches for {{ selected_event.name }}</h3>
    <p class="text-sm text-gray-500 mt-1">{{ proposed_matches|length }} matches generated</p>
</div>

<!-- NEW: Judge Selection Section -->
<div class="px-6 py-4 border-b border-gray-200">
    <label class="block text-sm font-medium text-gray-700 mb-2">
        Assign Judges to All Matches <span class="text-red-600">*</span> (Minimum 3)
    </label>
    <div class="space-y-2 max-h-48 overflow-y-auto border border-gray-300 rounded-lg p-3">
        {% for judge in judges %}
        <label class="flex items-center p-2 hover:bg-gray-50 rounded cursor-pointer">
            <input type="checkbox" name="judges" value="{{ judge.id }}" ...>
            <span class="ml-3 text-sm text-gray-700">
                {{ judge.profile.user.get_full_name|default:judge.profile.user.username }}
                <span class="text-gray-500">({{ judge.get_certification_level_display }})</span>
            </span>
        </label>
        {% endfor %}
    </div>
    <p class="mt-1 text-xs text-gray-500">Select the judges who will officiate all auto-matched games. These judges will be assigned to each created match.</p>
</div>

<!-- ... matches table ... -->

<!-- NEW: Submit Button Section -->
<div class="px-6 py-4 border-t border-gray-200 flex items-center justify-end">
    <button type="submit" ...>
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
        </svg>
        Create Selected Matches
    </button>
</div>
```

Changes:
- Moved form submission header content
- Added new judge selection section with checkboxes
- All checkboxes submit with name="judges"
- Moved submit button to bottom with better visibility
- Added helpful text about judges being assigned to all matches

## Validation Logic

### Judge Count Validation
```python
# Filter out empty strings and count valid judge IDs
valid_judges = [j for j in judge_ids if j]
is_valid = len(valid_judges) >= 3
```

### Error Messages
| Scenario | Message |
|----------|---------|
| Form submission with <3 judges | "At least 3 judges must be selected" |
| Auto-match with <3 judges | "At least 3 judges must be selected for auto-matched games." |
| Insufficient judges + conflicts | Judge conflict error takes precedence |

## Data Flow

### Manual Match Creation
```
Form Submit → Judge validation (3+ required)
           → Judge conflict validation
           → Create Match
           → Create MatchJudge entries
           → Redirect with success message
```

### Auto-Matching
```
Event Selection → Generate proposals
              ↓
    Display matches + judge selector
              ↓
Form Submit → Judge validation (3+ required)
           ↓
    For each selected match:
        → Judge conflict validation
        → Create Match
        → Create MatchJudge entries (same judges for all)
              ↓
        Redirect with success message
```

## Testing Examples

### ✅ Valid: Manual match with 3 judges
```python
judges_selected = [judge1, judge2, judge3]
len(judges_selected) >= 3  # True
# Match created successfully
```

### ✅ Valid: Auto-match with 5 judges for multiple matches
```python
judges_selected = [judge1, judge2, judge3, judge4, judge5]
len(judges_selected) >= 3  # True
# Each of 5 judges assigned to each created match
```

### ❌ Invalid: Manual match with 2 judges
```python
judges_selected = [judge1, judge2]
len(judges_selected) >= 3  # False
# Error: "At least 3 judges must be selected"
```

### ❌ Invalid: Auto-match with 0 judges
```python
judges_selected = []
len(judges_selected) >= 3  # False
# Error: "At least 3 judges must be selected for auto-matched games."
# Redirect back to auto-matching page
```

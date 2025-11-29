# Minimum Judges Implementation for Matches

## Overview
This implementation ensures that every match created (both manually and through auto-matching) must have at least 3 judges assigned. This enforces the requirement across all match creation workflows.

## Changes Made

### 1. Matchmaking Service (`core/services/matchmaking.py`)
- Added constant `MIN_JUDGES_REQUIRED = 3` to the `MatchmakingService` class
- Updated `assign_judges()` method to validate that at least 3 judges are provided before assigning them

### 2. Manual Match Creation (`core/views/admin.py`)

#### match_add() view
- Added validation to check that at least 3 judges are selected when creating a new match
- Error message: "At least 3 judges must be selected"
- Form validation occurs before attempting to create the match

#### match_edit() view
- Added the same 3-judge minimum validation for editing existing matches
- Prevents updating a match without maintaining the 3-judge requirement

### 3. Auto-Matchmaking Workflow

#### auto_matchmaking() view
- Updated to pass judges list to the template for selection
- Allows admins to select judges before confirming auto-matched games

#### auto_matchmaking_confirm() view
- Added judge selection from POST data
- Validates that at least 3 judges are selected
- If less than 3 judges: shows error message and redirects back to auto-matching
- If valid: assigns the selected judges to ALL created matches
- Success message includes count of judges assigned

### 4. UI Templates

#### form.html (Manual Match Creation/Edit)
- Updated judge selection label to include required indicator (*)
- Added "(Minimum 3)" text next to label
- Shows error message if validation fails
- Displays helpful text: "Select at least 3 judges to officiate this match"
- Highlights section in red if there's a validation error

#### auto.html (Auto-Matchmaking)
- Added new "Judge Selection" section before the matches table
- Judges section appears after event selection and before proposed matches
- Displays all active judges with their certification levels
- Includes required indicator and minimum 3 note
- Helpful text explains judges will be assigned to all created matches
- Submit button only appears after both match proposals and judge selection are visible

## User Flow

### Manual Match Creation
1. Admin fills out match form (event, competitors, scheduled time)
2. Admin **must select at least 3 judges** from the checkbox list
3. If fewer than 3 judges selected → form shows error and prevents submission
4. If 3+ judges selected → match is created with judges assigned

### Manual Match Editing
1. Admin opens existing match for editing
2. Admin **must maintain at least 3 judges** in the selection
3. Same validation and error handling as creation
4. Judge list can be modified but must have minimum 3

### Auto-Matchmaking
1. Admin selects event → proposed matches are generated
2. Admin **must select at least 3 judges** from the judge list
3. Admin selects which proposed matches to create
4. Admin clicks "Create Selected Matches"
5. If fewer than 3 judges selected → shows error message, returns to auto-matching page
6. If 3+ judges selected → all selected matches created with judges assigned
7. Success message shows: "X matches created with Y judges assigned"

## Validation Rules

- **Manual Creation**: Exactly at match creation time
- **Manual Edit**: At match update time
- **Auto-Matching**: At confirmation time, before any matches are created

## Error Handling

### Scenarios Handled
1. No judges selected → "At least 3 judges must be selected"
2. 1-2 judges selected → "At least 3 judges must be selected"
3. Less than 3 valid judges selected (empty values filtered) → "At least 3 judges must be selected"
4. Judges with conflicts (competing in same event) → Existing conflict validation still applies

## Database Changes
No database schema changes required. Uses existing:
- `MatchJudge` model for judge-match relationships
- `Match` model for match records
- `Judge` model for judge information

## Testing Checklist

- [ ] Create match without judges → error shown
- [ ] Create match with 1 judge → error shown
- [ ] Create match with 2 judges → error shown
- [ ] Create match with 3 judges → success
- [ ] Create match with 5 judges → success
- [ ] Edit match with 2 judges → error shown
- [ ] Edit match with 3+ judges → success
- [ ] Auto-match without judge selection → error shown
- [ ] Auto-match with 2 judges → error shown
- [ ] Auto-match with 3+ judges → all matches created with judges assigned
- [ ] Judge conflicts still prevented → conflict validation still works

## Benefits

1. **Fairness**: Every match has 3 judges to evaluate and score
2. **Consistency**: Same rule applied to all match types (manual and auto)
3. **Data Integrity**: No matches can be created without proper official oversight
4. **User Experience**: Clear error messages guide admins to comply

## Future Enhancements

1. Allow configurable minimum judge count (currently hardcoded to 3)
2. Add judge filtering by certification level for a match
3. Auto-suggest judges based on availability
4. Prevent double-assignment of same judge to multiple concurrent matches
5. Add notification when judges are assigned to matches

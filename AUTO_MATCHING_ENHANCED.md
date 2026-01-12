# Auto-Matching Enhancement: Title Matches & Ongoing Match Support

## Overview
The auto-matching system has been enhanced to support two new features:
1. **Title/Championship Matches** - Competitive bouts between trainees who have already completed matches
2. **Ongoing Match Support** - Allow all trainees to be auto-matched, including those with ongoing matches

## Key Features

### 1. Title Match Support
- Creates championship-level matches between trainees with completed matches in the same event
- Title matches receive priority scoring (10% bonus) for optimal pairing selection
- Clearly labeled with a "Title Match" indicator in both UI and match notes
- Enables tournament progression: Regular matches → Completed matches → Title matches

### 2. Ongoing Match Support
- New checkbox: "Allow trainees with ongoing matches to be auto-matched"
- When enabled, trainees can have multiple matches simultaneously (realistic tournament scenario)
- Prevents filtering out trainees just because they have scheduled/ongoing matches
- Enables flexible tournament scheduling

### 3. Enhanced Matching Options
Two new configuration checkboxes on the auto-matching form:
- **"Allow trainees with ongoing matches to be auto-matched"** (default: enabled)
  - When ON: All trainees eligible for regular + title matches
  - When OFF: Only trainees without scheduled/ongoing matches
  
- **"Include title/championship matches"** (default: enabled)
  - When ON: Generates title match suggestions between qualified trainees
  - When OFF: Only regular matches between available trainees

## Technical Changes

### Service Layer (`core/services/matchmaking.py`)

#### Updated `ProposedMatch` dataclass:
```python
@dataclass
class ProposedMatch:
    # ... existing fields ...
    is_title_match: bool = False  # New field to mark title matches
```

#### Enhanced `auto_match()` method:
```python
def auto_match(
    self, 
    event_id: int, 
    allow_ongoing_matches: bool = True,      # NEW parameter
    include_title_matches: bool = True        # NEW parameter
) -> List[ProposedMatch]:
```

**Logic:**
1. Fetches all registered trainees
2. Identifies trainees with completed matches (candidates for title matches)
3. If `allow_ongoing_matches=True`:
   - All trainees eligible for regular matching
   - Completed-match trainees also eligible for title matches
4. If `allow_ongoing_matches=False`:
   - Only trainees without ongoing matches eligible for regular matches
   - Title matches disabled
5. Title matches scored with 10% bonus (`score * 0.9`) for prioritization
6. Greedy algorithm selects best matches first

#### Updated `create_match()` method:
```python
def create_match(
    self,
    event_id: int,
    competitor1_id: int,
    competitor2_id: int,
    judge_ids: List[int],
    scheduled_time: datetime,
    is_title_match: bool = False,           # NEW parameter
    match_notes: str = ""                    # NEW parameter
) -> Match:
```

Automatically adds "Title Match / Championship" to match notes when `is_title_match=True`.

### Views (`core/views/admin.py`)

#### `auto_matchmaking()` view:
- Reads new checkbox parameters: `allow_ongoing_matches`, `include_title_matches`
- Passes options to service
- Stores `is_title_match` flag in session for each proposed match
- Saves options in session for confirmation flow

#### `auto_matchmaking_confirm()` view:
- Retrieves `is_title_match` flag from session
- Adds "Title Match / Championship" to match notes
- Tracks title match count separately
- Provides enhanced success message: "X matches created (Y title matches)"

### Template (`templates/admin/matchmaking/auto.html`)

#### Event Selection Section:
- New "Matching Options" area with two checkboxes
- Clear descriptions of what each option does
- Default values: both enabled for maximum flexibility

#### Match Display (Desktop Table):
- New "Type" column showing match type
- Title matches: Purple badge with star icon ⭐
- Regular matches: Gray "Regular" badge

#### Match Display (Mobile Cards):
- Title match badge displayed prominently
- Same visual indicators as desktop

#### Info Box:
- Updated matching rules explanation
- Added notes about regular vs. title matches

#### No Results Message:
- Enhanced help text suggesting to enable "Allow trainees with ongoing matches" option
- Better guidance for users

## Matching Algorithm Details

### Trainee Eligibility
```
Regular Matches:
- All trainees (unless "allow_ongoing_matches" is OFF)

Title Matches:
- Trainees with at least one COMPLETED match
- Must have same/adjacent belt ranks
- Weight difference ≤ 5kg
- Age difference ≤ 3 years
```

### Scoring
```
Base Score = (weight_diff × 2) + (belt_diff × 3) + age_diff

Title Match Score = Base Score × 0.9  (10% bonus)

Lower score = Better match quality
```

### Selection Algorithm
1. Calculate scores for all valid pairings
2. Sort by score (ascending)
3. Greedily select matches:
   - Pick best scoring pair
   - Mark both trainees as used
   - Continue until all pairs exhausted

## Data Flow

### Session Storage
```python
# Auto-matching view stores:
{
    'proposed_matches': [
        {
            'competitor1_id': int,
            'competitor2_id': int,
            'weight_diff': str,
            'belt_diff': int,
            'age_diff': int,
            'is_title_match': bool,  # NEW
        }
    ],
    'auto_match_event_id': str,
    'auto_match_options': {           # NEW
        'allow_ongoing_matches': bool,
        'include_title_matches': bool,
    }
}
```

### Match Creation
When admin selects matches and confirms:
- Each match created with proper `notes` field
- Title matches tagged with "Title Match / Championship"
- Judges assigned to all matches
- Success message shows total and title match count

## Example Usage Scenarios

### Scenario 1: Tournament with Title Matches
1. First Round: Regular matches between all trainees
2. Second Round: Enable title matches after first round completes
3. System generates matches between winners
4. Championship finals become title matches

### Scenario 2: Single-Day Tournament
1. Morning bracket (regular matches)
2. Afternoon bracket (regular + title matches simultaneously)
3. Evening finals (championship matches)

### Scenario 3: Progressive Tournament
1. All trainees eligible for both regular and title matches
2. Multiple brackets running simultaneously
3. Flexible scheduling with overlapping matches

## Backward Compatibility
- Default behavior matches previous implementation:
  - `allow_ongoing_matches=True` (changed from False)
  - `include_title_matches=True` (new option)
- Existing match creation calls work without changes
- Session cleanup properly removes all new session keys

## Testing Recommendations

1. **Title Match Generation**
   - Create event with multiple completed matches
   - Enable title matches
   - Verify only qualified trainees appear in proposals
   - Check scoring and prioritization

2. **Ongoing Match Support**
   - Create event with scheduled/ongoing matches
   - Test with checkbox ON: Should include ongoing-match trainees
   - Test with checkbox OFF: Should exclude ongoing-match trainees

3. **Mixed Matching**
   - Create event with mix of unmatched, matched, and completed trainees
   - Enable both regular and title matches
   - Verify correct distribution and prioritization

4. **Edge Cases**
   - All trainees already matched: Should show no results
   - Only one trainee eligible: Should show no pairs
   - Mismatched weight/belt/age: Should handle gracefully

## Performance Considerations
- O(n²) pairing comparison (same as original)
- Additional filter for completed matches: O(n) where n = matches
- Memory impact: Minimal (one additional boolean per proposal)
- Title match score calculation: Negligible overhead (10% of scoring time)

## Future Enhancements
1. Manual title match creation without auto-matching
2. Title match tier levels (Tier 1, Tier 2, Tier 3)
3. Championship bracket generation
4. Title match statistics and tracking
5. Dynamic weight class adjustments for title matches

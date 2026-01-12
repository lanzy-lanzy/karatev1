# Auto-Matching Enhancement - Quick Start Guide

## New Features

### 🏆 Title/Championship Matches
Create special "championship" matches between trainees who have already competed:
- Only trainees with **completed matches** are eligible
- Separate from regular tournament matches
- Marked with a special "★ Title Match" badge
- Automatically prioritized in match selection

### ⚡ Ongoing Match Support
Allow all trainees to be auto-matched, even if they have:
- Scheduled matches
- Ongoing/in-progress matches
- Multiple simultaneous matches

## How to Use

### Step 1: Go to Auto-Matchmaking
Admin Dashboard → Matchmaking → Auto-Matchmaking

### Step 2: Select Event & Options
1. Choose an event from the dropdown
2. Configure matching options:
   - ☑️ **"Allow trainees with ongoing matches"** (checked by default)
     - Enables all trainees to be matched
     - Allows title matches to be generated
   
   - ☑️ **"Include title/championship matches"** (checked by default)
     - Generates matches between qualified trainees
     - Uncheck if you only want regular matches

### Step 3: Generate Matches
Click **"Generate Matches"** button

### Step 4: Review & Select
- All proposed matches appear in a table
- Match type clearly shown: **★ Title Match** or **Regular**
- Review weight, belt rank, and age differences
- Select which matches to create (default: all selected)

### Step 5: Assign Judges & Create
1. Select at least **3 judges** for all matches
2. Click **"Create Selected Matches"**
3. Success message shows count and title match breakdown

## Match Types

### Regular Matches
- For trainees without ongoing matches (or all, if enabled)
- Standard tournament bracket matches
- Shown with **"Regular"** badge

### Title Matches ⭐
- Championship bouts between experienced competitors
- Requires trainees with at least one completed match
- Higher priority in automatic pairing
- Shown with **"★ Title Match"** badge
- Notes field automatically marked as "Title Match / Championship"

## Matching Rules (All Matches)
- **Weight:** Within 5kg difference
- **Belt Rank:** Same or adjacent (white-yellow, green-blue, etc.)
- **Age:** Within 3 years

## Configuration Examples

### Configuration 1: Standard Tournament
- ✓ Allow ongoing matches: **OFF**
- ✓ Include title matches: **OFF**
- Result: Only regular matches between unmatched trainees

### Configuration 2: Progressive Tournament
- ✓ Allow ongoing matches: **ON**
- ✓ Include title matches: **OFF**
- Result: All trainees can compete multiple times (regular matches only)

### Configuration 3: Championship Tournament
- ✓ Allow ongoing matches: **ON**
- ✓ Include title matches: **ON**
- Result: Regular matches + championship matches (recommended)

### Configuration 4: Finals Only
- ✓ Allow ongoing matches: **ON**
- ✓ Include title matches: **ON**
- Result: System proposes championship matches between winners (recommended for finals)

## Common Scenarios

### Scenario A: Multi-Round Tournament
**Round 1:** Generate regular matches (both checkboxes ON)
→ Matches created, trainees compete

**Between Rounds:** Wait for matches to complete

**Round 2:** Generate title matches (both checkboxes ON)
→ System prioritizes matches between winners

**Outcome:** Natural progression from regular → title matches

### Scenario B: Single-Day Event
**Morning:** Generate all matches with both checkboxes ON
**Result:** Mix of regular and title matches scheduled simultaneously
**Benefit:** Keeps all participants active throughout the day

### Scenario C: Practice Tournament
**Setup:** Only regular matches (turn OFF "Include title matches")
**Result:** Simple round-robin without championship tier
**Benefit:** Simpler logistics, equal experience level

## Troubleshooting

### Problem: "No valid matches found"
**Solutions:**
1. Enable "Allow trainees with ongoing matches" checkbox
2. Ensure trainees meet weight/belt/age constraints
3. Check that enough trainees are registered in the event
4. If looking for title matches: Ensure some trainees have completed matches first

### Problem: Not seeing title matches
**Check:**
1. Is "Include title/championship matches" checkbox enabled?
2. Do any trainees have completed matches in this event?
3. Do completed-match trainees meet weight/belt/age criteria?

### Problem: Too many matches generated
**Solutions:**
1. Turn OFF "Allow ongoing matches" to restrict to unmatched trainees only
2. Manually deselect some proposed matches before creating
3. Create matches in separate batches (different judge groups)

### Problem: Need more regular matches
**Solutions:**
1. Turn OFF "Include title matches" checkbox
2. This focuses algorithm on regular matches between available trainees

## Match Notes & Tracking

### Title Match Indicators
- **UI Badge:** Purple "★ Title Match" badge in match list
- **Match Notes:** Auto-filled with "Title Match / Championship"
- **Admin Panel:** Visible in match details and edit view

### Trainee Matching Status
Track trainee participation:
- Scheduled matches: Blue badge
- Ongoing matches: Orange badge  
- Completed matches: Green badge
- Can now have multiple matches simultaneously!

## Tips & Best Practices

✅ **DO:**
- Enable "Allow ongoing matches" for realistic tournament scenarios
- Use title matches for progression and championship tiers
- Review proposed matches before creation
- Assign experienced judges to title matches
- Create matches in batches for better scheduling

❌ **DON'T:**
- Create title matches without any completed matches first
- Disable both options expecting to get results
- Assign the same judge to overlapping matches
- Create too many simultaneous matches for small venues

## Advanced Options

### Manual Adjustment
After generating, you can:
- Deselect specific matches to exclude them
- Regenerate with different settings
- Select different judges for different batches

### Judge Assignment
- Different judge groups for different match types
- Rotate judges to avoid fatigue
- Assign senior judges to title matches for prestige

## API Reference (for developers)

See `AUTO_MATCHING_ENHANCED.md` for technical details on:
- Service method parameters
- Session data structure
- Scoring algorithm
- Database schema changes

---

**Last Updated:** December 2025
**System Version:** BlackCobra Karate Club v2.x

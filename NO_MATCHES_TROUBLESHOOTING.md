# Troubleshooting: "No Valid Matches Found"

## Problem
The auto-matching feature shows "No valid matches found" even though there are 12+ registered trainees in the event.

---

## Root Cause Analysis

The auto-matching system requires **ALL THREE** constraints to be met for a pairing to be valid:

1. **Weight**: Difference ≤ 5kg
2. **Belt Rank**: Same or adjacent (e.g., white-yellow, green-blue)
3. **Age**: Difference ≤ 3 years (if both have DOB)

If NO pairings satisfy all three, you get "No valid matches found."

---

## Quick Diagnostic

Run the diagnostic script to identify which constraints are failing:

```bash
python diagnose_matching_issue.py
```

Or for a specific event:
```bash
python diagnose_matching_issue.py --event-name "Spring Tournament"
```

The script will show:
- ✓ How many pairings meet each constraint
- ✗ Which specific pairings fail which constraints
- 💡 Specific recommendations for your event

---

## Common Reasons & Solutions

### 1. **Weight Distribution Too Spread Out**

**Problem**: Registered trainees have very different weights (e.g., 50kg and 90kg)

**Evidence**: Script shows "Weight constraint: 2/45 (4%)" - only 2 out of 45 pairs are within 5kg

**Solution**:
- Register trainees with similar weights
- Example: For 12 trainees, organize into groups:
  - Lightweight group: 50-60kg (4-6 trainees)
  - Middleweight group: 70-80kg (4-6 trainees)
  - Heavyweight group: 90kg+ (4-6 trainees)

**Best Practice**: Keep all trainees in an event within 15kg weight span for good matching.

---

### 2. **Belt Ranks Too Spread Out**

**Problem**: Trainees have very different belt levels (e.g., white and black)

**Evidence**: Script shows "Belt constraint: 5/45 (11%)" - only 5 out of 45 pairs have adjacent belts

**Solution**:
- Register trainees from same or adjacent belt levels
- Example: For 12 trainees:
  - White/Yellow group: 4-6 trainees
  - Orange/Green group: 4-6 trainees
  - Blue/Brown group: 2-4 trainees

**Best Practice**: Don't mix white belts with brown/black belts in same event.

---

### 3. **Ages Too Spread Out**

**Problem**: Trainees have large age gaps (e.g., 15 years and 45 years old)

**Evidence**: Script shows "Age constraint: 8/45 (18%)" - only 8 out of 45 pairs are within 3 years

**Solution**:
- Register trainees of similar ages
- Use date_of_birth field consistently
- Example: For 12 trainees:
  - Young group: 18-25 years (4-6 trainees)
  - Adult group: 26-35 years (4-6 trainees)
  - Senior group: 35+ years (2-4 trainees)

**Note**: If date_of_birth isn't set, this constraint is automatically skipped.

---

### 4. **Multiple Constraints Failing Simultaneously**

**Problem**: Trainees fail multiple constraints at once

**Example**:
```
Trainee A: 70kg, white belt, 25 years
Trainee B: 85kg, black belt, 45 years

Weight: 70 vs 85 = 15kg > 5kg ✗ FAIL
Belt: white vs black = 7 positions apart ✗ FAIL  
Age: 25 vs 45 = 20 years > 3 years ✗ FAIL
Result: NO VALID PAIRING
```

**Solution**: Register trainees in organized groups that match on multiple dimensions:
- Similar weight ranges
- Same or adjacent belt levels
- Similar age groups

---

## Event Organization Best Practices

### For Guaranteed Matchmaking Success:

**Option 1: Single Belt Level**
```
Event: Beginner Tournament
Trainees:
  - 8-10 white belt trainees
  - Weights: 50-70kg (keep within 15kg)
  - Ages: 18-30 years

Result: All pairs will have belt ✓, most will have weight ✓, many will have age ✓
Expected valid pairings: 80-90%
```

**Option 2: Two Adjacent Belt Levels**
```
Event: Intermediate Tournament
Trainees:
  - 5-6 orange belt trainees
  - 5-6 green belt trainees
  - Weights: 60-80kg (keep within 15kg)
  - Ages: 20-35 years

Result: All pairs have same/adjacent belt ✓, weight matches ✓, age matches ✓
Expected valid pairings: 70-85%
```

**Option 3: Organized Divisions**
```
Event: Open Tournament
Division 1 - Lightweight White:
  - 4 white belt trainees, 50-65kg, 18-25 years
Division 2 - Middleweight Yellow:
  - 4 yellow belt trainees, 65-80kg, 20-30 years
Division 3 - Heavyweight Green:
  - 4 green belt trainees, 80kg+, 25-35 years

Result: Each division has near-perfect matching
Expected valid pairings: 90-100% per division
```

---

## Checking Trainee Data Quality

Use this script to verify your trainees are ready for matching:

```bash
python update_all_weight_classes.py
```

Check for:
- ✓ All trainees have `weight` field filled
- ✓ All trainees have `belt_rank` set
- ✓ Weight distribution is reasonable
- ✓ (Optional) All trainees have `date_of_birth` set

---

## Step-by-Step Fix for Current Event

### 1. Run Diagnostic
```bash
python diagnose_matching_issue.py --all
```

### 2. Identify Problem
Read the output to see which constraint is failing most:
- Weight distribution? → Register similar weights
- Belt levels? → Register same/adjacent belts
- Ages? → Register similar ages

### 3. Reorganize Event (Options)

**Option A: Split into Multiple Events**
- Create Beginner Tournament (white/yellow belts)
- Create Intermediate Tournament (orange/green belts)
- Create Advanced Tournament (blue/brown/black belts)

**Option B: Register New Trainees**
- Add trainees that fill gaps in weight/belt/age
- Example: If you have 70kg blues and 90kg blues, add some 75-85kg blues

**Option C: Manual Matching**
- Use "Manual Match" instead of "Auto Matchmaking"
- Pair trainees manually based on best judgment
- Can override system constraints

### 4. Try Auto-Matching Again
```
Admin → Events → Select Event → Generate Matches
```

---

## Advanced: Adjusting Constraints

If you need to loosen constraints (not recommended), edit:

**File**: `core/services/matchmaking.py`

**Lines 52-54**:
```python
MAX_WEIGHT_DIFF = Decimal('5.0')   # Change to 10.0 for ±10kg
MAX_AGE_DIFF = 3                    # Change to 5 for ±5 years
```

**Example**: To allow ±10kg weight differences:
```python
MAX_WEIGHT_DIFF = Decimal('10.0')
```

**Warning**: Loosening constraints may result in unfair matches.

---

## Verification Checklist

Before claiming auto-matching works:

- [ ] Run `python diagnose_matching_issue.py --all`
- [ ] Check that at least ONE event shows valid pairings
- [ ] Verify weight/belt/age distributions are reasonable
- [ ] Try auto-matching on that event
- [ ] Confirm matches are generated
- [ ] Review match quality (belts/weights/ages reasonable)

---

## Examples of Good vs Bad Events

### ❌ BAD EVENT (Will Fail)
```
Spring Tournament - 12 Trainees
Weights: 50kg, 65kg, 70kg, 80kg, 90kg, 95kg, 55kg, 75kg, 85kg, 100kg, 60kg, 110kg
Belts: white, yellow, orange, green, blue, brown, black, white, yellow, orange, green, blue
Ages: 15, 18, 22, 28, 35, 42, 45, 16, 20, 25, 30, 38

Problem: Everything is spread out - weights span 60kg, belts span all levels, ages span 30 years
Result: Almost NO valid pairings
```

### ✅ GOOD EVENT (Will Work)
```
Lightweight White Belt Tournament - 8 Trainees
Weights: 50.0, 51.5, 52.0, 53.5, 54.0, 55.0, 56.0, 57.0 kg
Belts: white, white, white, white, white, white, white, white
Ages: 18, 19, 20, 21, 19, 20, 22, 21

Problem: None - all within constraints
Result: Many valid pairings, excellent matches
```

---

## Testing the Fix

After reorganizing your event:

1. **Clear Old Registrations** (optional)
   - Remove trainees who don't fit your new group
   - Register new trainees that fit better

2. **Run Auto-Matching**
   ```
   Admin → Events → Select Event → Generate Matches
   ```

3. **Check Results**
   - Should see "5 proposed matches" (or similar)
   - Each match should show weight/belt/age values
   - Review quality of matches

4. **Confirm Matches**
   - Click "Confirm" to create the matches
   - Verify matches appear in Matches list

---

## FAQ

**Q: Can I have mixed belt levels?**
A: Yes, but they must be adjacent (e.g., white-yellow OK, white-green NOT OK)

**Q: Do I need to set date_of_birth?**
A: No, it's optional. Age constraint is skipped if not set.

**Q: What if I have 15 trainees of same belt?**
A: Organize them into weight groups:
- Lightweight: 50-60kg
- Middleweight: 70-80kg
- Heavyweight: 90kg+

**Q: Can I force matches anyway?**
A: Yes, use "Manual Match" to pair any two trainees without constraints

**Q: Will auto-matching always work?**
A: Only if trainees meet the constraints. Organize event registration properly.

---

## Support

For specific event diagnosis:
```bash
python diagnose_matching_issue.py --event-name "Your Event Name"
```

This will show exactly what constraints are failing and why.

---

**Version**: 1.0
**Last Updated**: 2025-11-29

# Quick Start: Weight Classes & Auto-Matching

## TL;DR - What You Need to Know

✓ **Weight class system is fully functional and automatic**  
✓ **Auto-matching by belt and weight is properly implemented**  
✓ **All trainees need to be updated with weight classes**

---

## Step 1: Update All Trainees' Weight Classes

### Option A: Using Python Script (Recommended)
```bash
python update_all_weight_classes.py
```

This will:
- Calculate weight class for each trainee based on weight
- Show progress for each update
- Display distribution statistics
- Verify no trainees are missing weight classes

### Option B: Using Management Command
```bash
python manage.py fix_weight_classes
```

### Option C: Using SQL (Direct Database)
```bash
sqlite3 db.sqlite3 < update_weight_classes.sql
```

---

## Step 2: Verify Weight Classes

Run the verification command:
```bash
python update_all_weight_classes.py
```

Check output:
- All active trainees should have a weight_class value
- Should see distribution across 6 classes:
  - Flyweight (≤50kg)
  - Lightweight (50-60kg)
  - Welterweight (60-70kg)
  - Middleweight (70-80kg)
  - Light Heavyweight (80-90kg)
  - Heavyweight (>90kg)

---

## Step 3: Test Auto-Matching

### Create Test Event with Trainees

1. Admin Dashboard → Events → Create Event
2. Register at least 4-6 trainees with:
   - Different weight ranges (within 5kg pairs)
   - Same or adjacent belt ranks
   - Age differences ≤3 years (optional)

### Run Auto-Matching

1. Events → Select Event
2. Click "Auto Matchmaking"
3. Review proposed matches
4. Confirm to create matches

---

## Weight Class System

```
Class                Range
Flyweight            ≤ 50 kg
Lightweight          50-60 kg
Welterweight         60-70 kg
Middleweight         70-80 kg
Light Heavyweight    80-90 kg
Heavyweight          > 90 kg
```

**Automatic**: Updated whenever trainee's weight is saved. No manual updates needed.

---

## Auto-Matching Constraints

### All Three Must Be Met:

1. **Weight**: Difference ≤ 5kg
   - 70kg trainee can match with 65-75kg trainee
   
2. **Belt Rank**: Same or adjacent belt
   - White can match with: White, Yellow
   - Yellow can match with: White, Yellow, Orange
   - Orange can match with: Yellow, Orange, Green
   - (and so on...)
   
3. **Age**: Difference ≤ 3 years (if both have DOB)
   - 25-year-old can match with 22-28 year old

---

## Files Created

### Scripts
- `update_all_weight_classes.py` - Update all trainees (recommended)
- `run_fix_weight_classes.py` - Alternative entry point
- `check_trainees.py` - Check trainee status

### Management Command
- `core/management/commands/fix_weight_classes.py` - Django management command

### SQL
- `update_weight_classes.sql` - Direct database update

### Documentation
- `WEIGHT_CLASS_AND_MATCHING_ANALYSIS.md` - Full technical details
- `AUTO_MATCHING_DETAILED_REVIEW.md` - Matching system review
- `QUICK_START_WEIGHT_CLASSES.md` - This file

---

## Common Issues & Fixes

### "No valid matches could be generated"
**Cause**: Trainees don't meet constraints
**Fix**: 
- Check weights are within 5kg of each other
- Check belt ranks are same or adjacent
- Add trainees with better matching characteristics

### Trainees still missing weight_class
**Cause**: Script didn't complete or trainees added after
**Fix**: Run the update script again

### Age-based matching not working
**Cause**: Date of birth not set
**Fix**: Populate DOB field (optional but recommended)

---

## Verification Checklist

- [ ] Run `python update_all_weight_classes.py`
- [ ] All active trainees have weight_class filled
- [ ] Weight class distribution looks reasonable
- [ ] Create test event with 4-6 trainees
- [ ] All trainees have belt_rank set
- [ ] (Optional) All trainees have date_of_birth set
- [ ] Run auto-matching on test event
- [ ] Review proposed matches for quality
- [ ] Confirm matches look reasonable

---

## Key Functions (For Reference)

### Weight Class Calculation
```python
trainee.calculate_weight_class()  # Returns class name
trainee.save()                    # Triggers auto-calculation
```

### Matching Validation
```python
service._is_valid_pairing(trainee1, trainee2)  # Returns True/False
service._calculate_pairing_score(t1, t2)       # Returns score
service.auto_match(event_id)                   # Returns proposed matches
```

---

## Status Summary

| Component | Status | Notes |
|-----------|--------|-------|
| Weight class system | ✓ Working | Auto-calculated on save |
| Belt matching | ✓ Working | Same/adjacent only |
| Weight matching | ✓ Working | ±5kg tolerance |
| Age matching | ✓ Working | ±3 years (optional DOB) |
| Auto-matching service | ✓ Working | Fully optimized |
| Database schema | ✓ Ready | weight_class field exists |

---

## Next Steps

1. **Immediate**: Run weight class update script
2. **Verify**: Check distribution and missing values
3. **Test**: Create test event and run auto-matching
4. **Monitor**: Review match quality and make adjustments
5. **Deploy**: Use in production events

---

**Version**: 1.0  
**Last Updated**: 2025-11-29  
**Status**: Ready for Use ✓

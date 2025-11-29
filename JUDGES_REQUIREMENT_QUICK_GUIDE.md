# Minimum Judges Requirement - Quick Guide

## What Changed?
Every match must now have **at least 3 judges** assigned. This applies to:
- ✅ Manual match creation
- ✅ Manual match editing  
- ✅ Auto-matchmaking confirmation

## How It Works

### Creating a Match (Manual)
```
1. Fill out form: Event, Competitor 1, Competitor 2, Scheduled Time
2. SELECT AT LEAST 3 JUDGES from the checkbox list
3. Click "Create Match"
```

**If you select fewer than 3 judges:**
```
⚠️ Error: "At least 3 judges must be selected"
   Form will not submit until you select 3+ judges
```

### Editing a Match
```
1. Open the match editing form
2. Update details as needed
3. MAINTAIN AT LEAST 3 JUDGES in selection
4. Click "Update Match"
```

### Auto-Matchmaking
```
1. Select Event
2. Click "Generate Matches" (proposed matches appear)
3. SELECT AT LEAST 3 JUDGES from the judge list
4. Check which proposed matches to create
5. Click "Create Selected Matches"
```

**If you select fewer than 3 judges:**
```
⚠️ Error: "At least 3 judges must be selected for auto-matched games"
   Must go back and select 3+ judges before trying again
```

## What Happens After?

Once a match is created with judges:
- Each selected judge is assigned to the match
- Judges can see the match in their dashboard
- The match shows all assigned judges in the admin view
- All 3+ judges can enter results when the match completes

## Key Points

| Item | Details |
|------|---------|
| **Minimum Judges** | 3 per match |
| **Maximum Judges** | Unlimited (select as many as needed) |
| **Judge Conflicts** | Still prevented (can't be competitor in same event) |
| **Manual Creation** | Validation at creation time |
| **Auto-Matching** | Validation at confirmation time |

## Troubleshooting

### Problem: Can't create match - says need 3 judges
**Solution:** Scroll through the judges list and select at least 3 checkboxes

### Problem: Some judges are greyed out
**Note:** This shouldn't happen, but if it does, those judges may have conflicts. Select other judges.

### Problem: Auto-match says error about judges
**Solution:** Go back to the matches list, the proposed matches are still saved. Select 3+ judges and try again.

## Admin Checklist

Before clicking Create/Submit:
- [ ] Event selected
- [ ] Two different competitors selected
- [ ] Scheduled time set
- [ ] **At least 3 judges selected** ← NEW REQUIREMENT
- [ ] (For auto-match) Selected which matches to create

## Notes for Admins

- The form will **prevent submission** if less than 3 judges selected
- You'll see helpful text: "Select at least 3 judges to officiate this match"
- For auto-matching, same judges are assigned to ALL selected matches
- You can assign as many judges as needed (3+)
- All assigned judges will receive the match in their dashboard

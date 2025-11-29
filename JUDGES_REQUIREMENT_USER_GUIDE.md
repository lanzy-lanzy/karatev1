# Minimum 3 Judges Requirement - User Guide for Admins

## Quick Answer
**Every match must have at least 3 judges assigned.**

## Where This Applies

✅ Creating a new match manually  
✅ Editing an existing match  
✅ Creating matches through auto-matchmaking  

## Manual Match Creation

### Step-by-Step

**1. Go to Matches → Add New Match**

You'll see a form with:
- Event (dropdown)
- Competitor 1 (dropdown)
- Competitor 2 (dropdown)
- Scheduled Time (date/time picker)
- **Assign Judges** (NEW requirement) ← See "Minimum 3" label

**2. Fill out the basic match details**

Select the event, two competitors, and when the match should happen.

**3. Select at least 3 judges**

Scroll through the "Assign Judges" section and check at least 3 judges:
```
☐ Judge 1 (Regional)
☐ Judge 2 (National)
☐ Judge 3 (International)
☐ Judge 4 (Regional)
```

**4. Click "Create Match"**

If you selected 3+ judges → Success! Match created.  
If you selected fewer than 3 → Error message:
```
❌ Error: "At least 3 judges must be selected"
```
The form will stay filled out, and you can add more judges.

---

## Manual Match Editing

### Similar to Creation

When editing an existing match, the same rules apply:

**1. Open the match to edit**

**2. Update any details**

Change event, competitors, or time as needed.

**3. Maintain 3+ judges**

Make sure you keep at least 3 judges selected:
- Can't reduce below 3
- Can add more judges
- Can remove judges (but must keep 3+)

**4. Click "Update Match"**

If you have 3+ judges → Success!  
If fewer → Error message, try again.

---

## Auto-Matchmaking Process

This is a 3-step process:

### Step 1: Select Event & Generate

1. Go to Matches → Auto-Matchmaking
2. Select an event from the dropdown
3. Click "Generate Matches"
4. The system proposes matches based on weight, belt, and age

### Step 2: Select Judges ⭐ NEW!

After matches are proposed, you'll see:

```
┌─ Assign Judges to All Matches * (Minimum 3) ─┐
│                                               │
│ ☐ Judge Sarah (Regional)                    │
│ ☐ Judge Ahmed (National)                    │
│ ☐ Judge Maria (International)               │
│ ☐ Judge Kenji (Regional)                    │
│ ☐ Judge Lisa (National)                     │
│                                               │
│ Note: These judges will be assigned to     │
│ each created match.                         │
└───────────────────────────────────────────────┘
```

**Important**: Select at least 3 judges. These judges will officiate **all** the matches you create.

### Step 3: Select Matches & Create

1. Check which proposed matches to create
2. Click "Create Selected Matches"

**If you forgot to select judges:**
```
❌ Error: "At least 3 judges must be selected for auto-matched games"
```
Go back and select 3+ judges, then try again.

**If you selected 3+ judges:**
```
✅ Success: "5 matches created with 3 judges assigned"
```

---

## What You'll See

### ✅ When It Works (3+ Judges)

**Form:**
```
Assign Judges * (Minimum 3)
┌──────────────────┐
│ ☑ Judge 1        │  ← Checked
│ ☑ Judge 2        │  ← Checked
│ ☑ Judge 3        │  ← Checked
│ ☐ Judge 4        │  ← Unchecked
└──────────────────┘
Select at least 3 judges to officiate this match

[Create Match] ← Button is clickable
```

**Success Message:**
```
✅ Match has been created successfully
```

---

### ❌ When It Fails (<3 Judges)

**Form:**
```
Assign Judges * (Minimum 3)
┌──────────────────┐
│ ☑ Judge 1        │  ← Only 2 selected
│ ☑ Judge 2        │  ← Only 2 selected
│ ☐ Judge 3        │
│ ☐ Judge 4        │
└──────────────────┘
Error: At least 3 judges must be selected ← Red error message
```

**Form stays on same page** so you can add more judges and try again.

---

## Pro Tips

### ✅ Do's

- ✅ Select 3 judges for balance
- ✅ Select 5 judges for major events
- ✅ Mix different certification levels (Regional, National, International)
- ✅ You can select more than 3 if needed
- ✅ Check judge availability before assigning

### ❌ Don'ts

- ❌ Don't try to create match with 0 judges
- ❌ Don't try to create match with 1 judge
- ❌ Don't try to create match with 2 judges
- ❌ Don't assign competing judges (system prevents this)
- ❌ Don't assign inactive judges

---

## Common Scenarios

### Scenario 1: Create Single Match

```
Admin Creates Match
         ↓
Selects 3 judges (Judge A, Judge B, Judge C)
         ↓
Clicks "Create Match"
         ↓
Match created, all 3 judges assigned
         ↓
Each judge sees match in their dashboard
```

### Scenario 2: Create Multiple Matches via Auto-Matching

```
Admin Does Auto-Matching
         ↓
Selects Event & Generates 5 proposed matches
         ↓
Selects 3 judges (Judge A, Judge B, Judge C)
         ↓
Checks boxes for 3 of the 5 proposed matches
         ↓
Clicks "Create Selected Matches"
         ↓
3 matches created, each with all 3 judges assigned
         ↓
Each judge sees 3 new matches in their dashboard
```

### Scenario 3: Edit Existing Match

```
Admin Edits Existing Match
         ↓
Currently has 2 judges assigned
         ↓
Tries to save with only 2 judges
         ↓
Error: "At least 3 judges must be selected"
         ↓
Admin adds 1 more judge (now has 3)
         ↓
Clicks "Update Match"
         ↓
Success! Match updated with 3 judges
```

---

## Judge Selection Reference

### Judge Certification Levels
- **Regional**: Can judge regional tournaments
- **National**: Can judge national tournaments
- **International**: Can judge international tournaments

### When Creating Matches
Pick a mix for variety:
- At least 1 high-level judge (National or International)
- Mix of experience levels
- Balance if possible

---

## Troubleshooting

### Q: "Error: At least 3 judges must be selected" appears

**A:** You need to select more judges. Scroll through the list and check at least 3 judge checkboxes.

### Q: Can I create a match with 0 judges?

**A:** No, the form won't allow it. You must select 3+ judges.

### Q: Can I assign the same judge to multiple matches?

**A:** Yes! One judge can be assigned to many matches.

### Q: Can I create a match with 10 judges?

**A:** Yes, if you want! But you need at least 3. More judges is fine.

### Q: What if I forget to select judges in auto-matchmaking?

**A:** You'll see an error message. Go back and select judges, then try creating again. Your match proposals are saved.

### Q: Can judges officiate if they're also competing?

**A:** No, the system prevents this. A judge can't be both a competitor and judge in the same event.

### Q: Do all 3 judges need to be at the same certification level?

**A:** No, you can mix levels. For example:
- 1 Regional + 1 National + 1 International ✅
- 3 National ✅
- 2 Regional + 1 International ✅

---

## Key Numbers to Remember

| Aspect | Rule |
|--------|------|
| **Minimum judges per match** | 3 |
| **Maximum judges per match** | Unlimited |
| **Judges for auto-match** | Same 3+ for all selected matches |

---

## Still Have Questions?

For technical issues or questions about implementation, see:
- `JUDGES_REQUIREMENT_QUICK_GUIDE.md`
- `JUDGES_IMPLEMENTATION_DETAILS.md`
- Code comments in admin views

For help with the system, contact the administrator.

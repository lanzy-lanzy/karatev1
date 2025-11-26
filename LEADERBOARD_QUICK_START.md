# Leaderboard & Belt Rank System - Quick Start

## Installation Status: ✅ COMPLETE

The belt rank and leaderboard system is **fully installed and ready to use**.

## What You Get

A complete points-based ranking system where trainees:
- Earn points by participating in karate events/matches
- Get automatically promoted to higher belt ranks when reaching point thresholds
- Compete on leaderboards (all-time, yearly, monthly, by belt rank)
- Track their progress toward the next belt rank

## Point System

| Result | Points |
|--------|--------|
| Win in match | +30 |
| Loss in match | +10 |

## Belt Ranks & Point Thresholds

| Belt | Points Required |
|------|-----------------|
| White | 0 |
| Yellow | 150 |
| Orange | 350 |
| Green | 600 |
| Blue | 900 |
| Brown | 1,300 |
| Black | 1,800 |

## Accessing the System

### View Leaderboards

Click these links or paste in browser:

- **All-Time Rankings**: `/leaderboard/all-time/`
- **This Year**: `/leaderboard/yearly/`
- **This Month**: `/leaderboard/monthly/`
- **By Belt Rank**: `/leaderboard/by-belt/`

### View Individual Trainee

Go to: `/trainee/<trainee_id>/points/`

Shows:
- Total points earned
- Wins and losses
- Progress to next belt rank with % bar
- Complete promotion history

### System Overview

Go to: `/belt-rank/progress/`

Shows:
- All belt thresholds
- Recent promotions
- How the system works

## How It Works

### Automatic Point Award

When a **judge submits a match result**:

```
1. Judge logs in → /judge/results/
2. Views assigned matches
3. Selects winner and enters scores
4. Submits result
5. System automatically:
   - Awards +30 points to winner
   - Awards +10 points to loser
   - Checks for belt rank promotion
   - Updates all leaderboards
```

**No additional steps needed!** Points are awarded automatically.

### Automatic Promotion

When a trainee reaches the next belt threshold:

```
Example: Blue belt trainee (900 pts needed for brown)
- Has: 870 points
- Wins 3 matches: +30 each = +90 points
- New total: 960 points
- Promotion triggered? YES (960 >= 900)
- Belt updated: Blue → Brown ✅
- Trainee can see promotion in their profile
```

## Using as Admin

### View All Models

Go to: `/admin/`

Click "Core" → Access:
- **Belt Rank Thresholds** - Edit point requirements
- **Trainee Points** - View stats (total points, wins, losses)
- **Belt Rank Progress** - See all promotions history
- **Leaderboard** - View rankings data

### Change Point Values

Option 1 - Via Admin UI:
```
1. Go to /admin/core/trainepoints/
2. Click a trainee's points record
3. Edit values
4. Save
```

Option 2 - Python:
```python
from core.models import BeltRankThreshold
# Update brown belt threshold
BeltRankThreshold.objects.filter(belt_rank='brown').update(points_required=1500)
```

### Change Belt Thresholds

In `/admin/core/beltrankthreshold/`:
- Click each belt rank
- Edit `points_required` field
- Save changes

## Using as Trainee

### View Personal Progress

1. Go to `/trainee/<your_id>/points/`
2. See:
   - Total points earned
   - Wins/losses
   - Progress bar to next belt
   - Your promotion history with dates

### View Rankings

1. Go to `/leaderboard/all-time/`
2. See where you rank among all trainees
3. Switch views: Yearly, Monthly, or By Belt
4. Click "View Profile" to see other trainees

## Using as Judge

### Points Auto-Award (Already Built-In)

When you submit a match result:
1. Log in → Judge Dashboard
2. Go to "Results" → Assign result
3. Select winner, enter scores
4. Submit

**That's it!** Points are awarded automatically to both competitors.

## Testing the System

### Step 1: Create Test Data

```bash
# In Django admin or shell
from core.models import Trainee, Event, Match, MatchResult

# Verify trainees exist
trainees = Trainee.objects.all()
print(f"Available trainees: {trainees.count()}")
```

### Step 2: Submit a Match Result

1. Judge logs in: `/judge/results/`
2. Submit a match result (pick a winner)
3. Check trainee points updated: `/admin/core/trainepoints/`
4. Verify leaderboard changed: `/leaderboard/all-time/`

### Step 3: Test Promotion

1. Find a trainee close to belt threshold
2. Submit 5+ wins to push them over
3. Check their profile: `/trainee/<id>/points/`
4. Should see promotion in history

## Common Tasks

### Task 1: View Who's Winning This Month

```
Go to: /leaderboard/monthly/?year=2025&month=1
Shows: Top trainees for January 2025
```

### Task 2: Check Progress for a Trainee

```
Go to: /trainee/1/points/
Shows: That trainee's stats and progress bar
```

### Task 3: See Recent Promotions

```
Go to: /belt-rank/progress/
Shows: Latest belt promotions
```

### Task 4: Compare Blue Belts

```
Go to: /leaderboard/by-belt/?belt=blue
Shows: All blue belt trainees ranked by points
```

### Task 5: Award Points Manually (Advanced)

```python
from core.models import Trainee, TraineePoints

trainee = Trainee.objects.get(id=1)
points, _ = TraineePoints.objects.get_or_create(trainee=trainee)
points.total_points += 50
points.save()
```

## Database Structure

Four new models were added:

1. **BeltRankThreshold**
   - Defines point requirement per belt rank
   - 7 records (one per belt)

2. **TraineePoints**
   - One per trainee
   - Tracks: total_points, wins, losses, events_participated

3. **BeltRankProgress**
   - Many per trainee (one per promotion)
   - Records: old_belt_rank, new_belt_rank, points_earned, promoted_at

4. **Leaderboard**
   - Rankings for all timeframes
   - Filtered by: timeframe (all-time, yearly, monthly), belt_rank, year, month

## URLs Reference

```
Leaderboards:
  /leaderboard/all-time/
  /leaderboard/yearly/?year=2024
  /leaderboard/monthly/?year=2024&month=11
  /leaderboard/by-belt/?belt=blue

Trainee Profile:
  /trainee/<trainee_id>/points/

System Info:
  /belt-rank/progress/

Admin:
  /admin/core/beltrankthreshold/
  /admin/core/trainepoints/
  /admin/core/beltrankprogress/
  /admin/core/leaderboard/
```

## Troubleshooting

### Issue: No leaderboard data showing

**Check:**
1. Make sure trainees have submitted match results
2. Go to `/admin/core/trainepoints/` - should see trainee records
3. If empty, submit a match result to generate data

### Issue: Trainee not promoted despite having points

**Check:**
1. Are they at the exact threshold? Need >= required points
2. Was the match result saved? Check activity log
3. Are BeltRankThresholds initialized? Should be 7 records in admin

### Issue: Points not awarded after match result

**Check:**
1. Was result actually submitted? Check `/admin/core/matchresult/`
2. Is MatchResult.save() being called?
3. Check Django error logs

### Issue: Wrong point values

**Change in code:**
```python
# core/models.py - TraineePoints class
def add_win(self):
    self.total_points += 30  # ← Change this number
    
def add_loss(self):
    self.total_points += 10  # ← Change this number
```

## Files & Code Locations

| What | Where |
|------|-------|
| Models | `core/models.py` (lines 344+) |
| Views | `core/views/leaderboard.py` |
| Services | `core/services/leaderboard_service.py` |
| Admin | `core/admin.py` |
| Templates | `templates/leaderboard/` |
| Setup | `core/management/commands/initialize_belt_thresholds.py` |

## Documentation Files

- **BELT_RANK_AND_LEADERBOARD_GUIDE.md** - Complete reference (70+ sections)
- **LEADERBOARD_IMPLEMENTATION_SUMMARY.md** - Features overview
- **INTEGRATION_GUIDE_LEADERBOARD.md** - How it integrates with existing system
- **LEADERBOARD_QUICK_START.md** - This file

## Next Steps

### To Use Right Now:
1. ✅ System is installed
2. ✅ Setup is complete
3. Judge logs in and submits match results
4. Go to `/leaderboard/all-time/` to view rankings

### To Customize:
1. Edit point values in `core/models.py`
2. Edit belt thresholds in Django admin
3. Adjust templates in `templates/leaderboard/`

### To Add Features (Future):
- Seasonal leaderboards (quarters)
- Weight class rankings
- Streak tracking
- Charts and analytics
- Email notifications
- Export functionality

## Support

For detailed information, see:
- **How Points Work?** → BELT_RANK_AND_LEADERBOARD_GUIDE.md section "Points System"
- **How Promotions Work?** → BELT_RANK_AND_LEADERBOARD_GUIDE.md section "Belt Rank Promotions"
- **How to Customize?** → INTEGRATION_GUIDE_LEADERBOARD.md section "Customizing the System"

## Success Checklist

- [ ] I can view `/leaderboard/all-time/` in browser
- [ ] I can see belt thresholds in `/admin/core/beltrankthreshold/`
- [ ] I can see thresholds initialized (7 total, White=0, Black=1800)
- [ ] I submitted a match result as judge
- [ ] Points were awarded (check `/admin/core/trainepoints/`)
- [ ] Leaderboard updated with new points
- [ ] I can view trainee progress at `/trainee/<id>/points/`

When all checked, **you're ready to go!** 🎉

---

**System Status:** Production Ready ✅

**Last Updated:** November 26, 2025

**Version:** 1.0 Complete

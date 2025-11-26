# Belt Rank & Leaderboard System

## Overview

A complete points-based belt rank progression and competitive leaderboard system for the karate training application. Trainees earn points through event participation, get automatically promoted to higher belt ranks, and compete on real-time leaderboards.

## Quick Links

| Document | Purpose |
|----------|---------|
| **LEADERBOARD_QUICK_START.md** | Start here - setup & usage guide |
| **IMPLEMENTATION_COMPLETE_LEADERBOARD.md** | What was built & current status |
| **BELT_RANK_AND_LEADERBOARD_GUIDE.md** | Complete technical reference |
| **INTEGRATION_GUIDE_LEADERBOARD.md** | How it integrates with system |
| **LEADERBOARD_IMPLEMENTATION_SUMMARY.md** | Features overview |

## 30-Second Overview

```
Judge submits match result → Points awarded automatically
  ├─ Winner gets +30 points
  └─ Loser gets +10 points

Trainee reaches belt threshold → Automatic promotion
  ├─ Belt rank updated
  └─ Promotion recorded with date

View leaderboards → Real-time competitive rankings
  ├─ All-time, yearly, monthly views
  ├─ Filter by belt rank
  └─ See trainee profiles with progress bars
```

## Key Features

### Points System
- **Win**: +30 points
- **Loss**: +10 points (participation)
- **Auto-Awarded**: When judge submits match result

### Belt Ranks (7 Levels)
```
White (0 pts) → Yellow (150) → Orange (350) → Green (600) 
  → Blue (900) → Brown (1300) → Black (1800)
```

### Leaderboards
- **All-Time**: Overall lifetime rankings
- **Yearly**: Current year rankings
- **Monthly**: Current month rankings
- **By Belt**: Filter by rank level

### Automatic Promotion
When trainee points ≥ next belt threshold:
1. Belt rank updated instantly
2. Promotion recorded with timestamp
3. Trainee can view history in profile

## Getting Started

### 1. Verify Installation
```bash
# Check migrations applied
python manage.py migrate --list

# Initialize belt thresholds (one-time)
python manage.py initialize_belt_thresholds
```

### 2. Test the System
1. Go to `/admin/` → Core → Belt Rank Thresholds
   - Should see 7 records (White: 0, Yellow: 150, etc.)

2. Submit a match result as judge
   - Go to `/judge/results/`
   - Submit result for a match
   
3. Check points awarded
   - Go to `/admin/` → Core → Trainee Points
   - Winner should have +30 points, loser +10

4. View leaderboards
   - Go to `/leaderboard/all-time/`
   - Should see trainees ranked by points

### 3. Try Trainee Profile
```
Go to: /trainee/<trainee_id>/points/
Shows: Points, wins, losses, belt progress, promotion history
```

## Main URLs

```
/leaderboard/all-time/                      All-time rankings
/leaderboard/yearly/?year=2024              Year-specific rankings
/leaderboard/monthly/?year=2024&month=11    Month-specific rankings
/leaderboard/by-belt/?belt=blue             Rankings by belt rank
/trainee/<id>/points/                       Trainee profile & progress
/belt-rank/progress/                        System overview
/admin/core/beltrankthreshold/              Manage belt thresholds
/admin/core/trainepoints/                   View trainee stats
```

## How It Works

### Automatic Point Award (Already Built-In)

The system integrates with the existing judge result submission:

```python
# In judge/views.py result_entry():
# When judge submits a match result:
MatchResult.objects.create(
    match=match,
    judge=judge,
    winner=winner,
    competitor1_score=c1_score,
    competitor2_score=c2_score,
)
# ^ This automatically:
#   1. Awards points to winner/loser
#   2. Checks for promotion
#   3. Updates all leaderboards
```

**No code changes needed** - it works automatically!

### Point Award Flow
```
MatchResult.save() 
  → _award_match_points()
    → TraineePoints.add_win()/add_loss()
      → check_belt_rank_promotion()
        → Update belt rank if threshold reached
    → Update leaderboards
```

### Promotion Example
```
Trainee: Blue Belt, 870 points (needs 900 for brown)
Wins 3 matches: +30 × 3 = +90 points
New total: 960 points
Promotion triggered? YES (960 ≥ 900)
Result: Automatically promoted to Brown Belt ✅
```

## Customization

### Change Point Values
Edit `core/models.py`:
```python
class TraineePoints(models.Model):
    def add_win(self):
        self.total_points += 30  # ← Change this
    
    def add_loss(self):
        self.total_points += 10  # ← Change this
```

### Change Belt Thresholds
In Django admin (`/admin/core/beltrankthreshold/`):
- Click each belt rank
- Edit `points_required` value
- Save

Or via Python:
```python
from core.models import BeltRankThreshold
BeltRankThreshold.objects.filter(belt_rank='brown').update(points_required=1500)
```

## Common Tasks

### View All-Time Rankings
```
/leaderboard/all-time/
```

### Check Trainee Progress
```
/trainee/1/points/
Shows: Points, wins, losses, progress bar, promotion history
```

### Filter by Belt Rank
```
/leaderboard/by-belt/?belt=blue
Shows: All blue belt trainees ranked by points
```

### View This Month's Rankings
```
/leaderboard/monthly/
Shows: Current month rankings
```

### Award Points Manually (Admin)
```python
from core.models import TraineePoints
tp = TraineePoints.objects.get(trainee_id=1)
tp.total_points += 50
tp.save()
```

## Database Models

### BeltRankThreshold
Defines point requirement per belt rank:
```
- belt_rank: white, yellow, orange, green, blue, brown, black
- points_required: 0, 150, 350, 600, 900, 1300, 1800
```

### TraineePoints
Tracks trainee statistics:
```
- total_points: int
- wins: int
- losses: int
- events_participated: int
- updated_at: datetime
```

### BeltRankProgress
Records all promotions:
```
- old_belt_rank: previous rank
- new_belt_rank: new rank
- points_earned: int
- promoted_at: datetime
```

### Leaderboard
Rankings by timeframe:
```
- rank: 1, 2, 3, ...
- points: total points
- timeframe: all_time, yearly, monthly
- belt_rank: current belt
- year/month: filters (if applicable)
```

## Admin Interface

All models registered at `/admin/`:

1. **BeltRankThreshold** - Edit point requirements
2. **TraineePoints** - View trainee statistics
3. **BeltRankProgress** - View promotion history
4. **Leaderboard** - View rankings

## Templates

Located in `templates/leaderboard/`:
- `leaderboard.html` - Main ranking display
- `leaderboard_by_belt.html` - Belt-filtered rankings
- `trainee_profile_points.html` - Individual stats
- `belt_rank_progress.html` - System overview

## Services

### LeaderboardService
```python
LeaderboardService.update_all_leaderboards()
LeaderboardService.get_leaderboard('all_time')
LeaderboardService.get_trainee_rank(trainee, 'all_time')
```

### PointsService
```python
PointsService.get_trainee_points(trainee)
PointsService.get_trainee_win_rate(trainee)
PointsService.get_progress_percentage(trainee)
PointsService.get_next_belt_threshold(trainee)
```

## Troubleshooting

### Issue: No leaderboard data

**Check:**
- Did you run migrations? `python manage.py migrate`
- Did you initialize thresholds? `python manage.py initialize_belt_thresholds`
- Are there any match results? Submit one as judge

### Issue: Trainee not promoted

**Check:**
- Do they have enough points? Check `/admin/core/trainepoints/`
- Is threshold defined? Check `/admin/core/beltrankthreshold/`
- Were thresholds initialized correctly?

### Issue: Points not awarded

**Check:**
- Was result actually submitted? Check `/admin/core/matchresult/`
- Check Django error logs
- Verify `_award_match_points()` in core/models.py

## Files Structure

```
core/
├── models.py              ← BeltRankThreshold, TraineePoints, etc.
├── views/leaderboard.py   ← Leaderboard views
├── services/leaderboard_service.py ← Business logic
├── admin.py               ← Admin registrations
└── management/commands/
    └── initialize_belt_thresholds.py

templates/leaderboard/
├── leaderboard.html
├── leaderboard_by_belt.html
├── trainee_profile_points.html
└── belt_rank_progress.html
```

## System Status

✅ **PRODUCTION READY**

- [x] All models created and migrated
- [x] All views implemented
- [x] All templates created
- [x] Admin interface registered
- [x] Services created
- [x] Management commands ready
- [x] Documentation complete
- [x] Integrated with judge results
- [x] Automatic point award working
- [x] Automatic promotions working

## Documentation Files

| File | Contains |
|------|----------|
| **LEADERBOARD_QUICK_START.md** | Quick setup & usage (start here) |
| **IMPLEMENTATION_COMPLETE_LEADERBOARD.md** | What was built & status |
| **BELT_RANK_AND_LEADERBOARD_GUIDE.md** | Complete technical guide |
| **INTEGRATION_GUIDE_LEADERBOARD.md** | Integration with system |
| **LEADERBOARD_IMPLEMENTATION_SUMMARY.md** | Features overview |
| **LEADERBOARD_README.md** | This file |

## Next Steps

### Immediate Use
1. ✅ System is ready to use
2. Go to `/leaderboard/all-time/` to see rankings
3. Judge submits match results as normal
4. Points awarded automatically
5. Trainees promoted when thresholds reached

### Customization
1. Change point values in `core/models.py`
2. Edit belt thresholds in `/admin/`
3. Modify templates in `templates/leaderboard/`

### Future Features
- Seasonal leaderboards (quarters)
- Weight class specific rankings
- Streak tracking (win/loss streaks)
- Email notifications on promotion
- Advanced analytics & charts
- CSV/PDF export

## Support

For detailed information, see the documentation files listed above.

**Recommended reading order:**
1. LEADERBOARD_QUICK_START.md (5 min)
2. IMPLEMENTATION_COMPLETE_LEADERBOARD.md (10 min)
3. BELT_RANK_AND_LEADERBOARD_GUIDE.md (reference)

---

**Version**: 1.0 Complete  
**Status**: ✅ Production Ready  
**Last Updated**: November 26, 2025

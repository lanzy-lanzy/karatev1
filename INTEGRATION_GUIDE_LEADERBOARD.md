# Leaderboard System Integration Guide

## Overview

The belt rank and leaderboard system is already **automatically integrated** into the existing application. Here's how everything connects:

## Automatic Integration Points

### 1. Judge Result Entry (Auto-Trigger)

When a judge submits a match result at `/judge/results/<match_id>/`:

```python
# In judge/views.py result_entry view (line 246)
MatchResult.objects.create(
    match=match,
    judge=judge,
    winner=winner,
    competitor1_score=competitor1_score,
    competitor2_score=competitor2_score,
    notes=notes,
    is_locked=True
)
```

This automatically triggers:
1. `MatchResult.save()` method
2. `_award_match_points()` executes
3. Winner gets +30 points
4. Loser gets +10 points
5. Automatic promotion check
6. Leaderboards update

**No code changes needed** - Just submit results as normal!

### 2. Database Migrations

All migrations have been applied:
```bash
python manage.py migrate
```

This created:
- `BeltRankThreshold` table
- `TraineePoints` table
- `BeltRankProgress` table
- `Leaderboard` table

### 3. Belt Thresholds Initialized

Run once to set up thresholds:
```bash
python manage.py initialize_belt_thresholds
```

Creates default thresholds (White: 0 pts, Yellow: 150 pts, etc.)

## Viewing the System

### Admin Interface
Access at `/admin/`:
- View all models in Django admin
- Manage belt thresholds
- View trainee points
- See promotion history

### User-Facing Views

All URLs are registered in `core/urls.py`:

1. **View All-Time Rankings**
   ```
   URL: /leaderboard/all-time/
   Shows: Top trainees overall
   ```

2. **View Yearly Rankings**
   ```
   URL: /leaderboard/yearly/?year=2024
   Shows: Top trainees for year 2024
   ```

3. **View Monthly Rankings**
   ```
   URL: /leaderboard/monthly/?year=2024&month=11
   Shows: Top trainees for November 2024
   ```

4. **View by Belt Rank**
   ```
   URL: /leaderboard/by-belt/?belt=blue
   Shows: Top blue belt trainees
   ```

5. **View Trainee Profile**
   ```
   URL: /trainee/<trainee_id>/points/
   Shows: Trainee's points, stats, progress, promotion history
   ```

6. **System Overview**
   ```
   URL: /belt-rank/progress/
   Shows: All belt thresholds and recent promotions
   ```

## How Points Flow Through the System

```
Match Happens
    ↓
Judge Submits Result
    ↓
MatchResult created/saved
    ↓
MatchResult.save() (line 287)
    ├─ Updates match.winner and status
    └─ Calls _award_match_points() (NEW!)
        ├─ Winner: TraineePoints.add_win() → +30 pts
        ├─ Loser: TraineePoints.add_loss() → +10 pts
        ├─ Check promotion
        │   └─ If threshold reached:
        │       ├─ Update trainee.belt_rank
        │       └─ Create BeltRankProgress entry
        └─ Update leaderboards
            ├─ all_time rankings
            ├─ yearly rankings
            └─ monthly rankings
    ↓
Points visible in:
    - /trainee/<id>/points/
    - /leaderboard/all-time/
    - Trainee's profile stats
```

## Database Queries

### View a Trainee's Points

```python
from core.models import TraineePoints

trainee = Trainee.objects.get(id=1)
points = TraineePoints.objects.get(trainee=trainee)
print(f"Points: {points.total_points}")
print(f"Wins: {points.wins}")
print(f"Losses: {points.losses}")
```

### Check Leaderboard Rank

```python
from core.models import Leaderboard

# Get all-time rank
rank = Leaderboard.objects.get(trainee=trainee, timeframe='all_time')
print(f"Rank #{rank.rank} with {rank.points} points")

# Get yearly rank
rank_2024 = Leaderboard.objects.get(trainee=trainee, timeframe='yearly', year=2024)
```

### Get Promotion History

```python
from core.models import BeltRankProgress

history = BeltRankProgress.objects.filter(trainee=trainee).order_by('-promoted_at')
for promotion in history:
    print(f"{promotion.old_belt_rank} → {promotion.new_belt_rank}")
    print(f"Promoted at: {promotion.promoted_at}")
```

## Using Services in Views

### In a Custom View

```python
from core.services.leaderboard_service import LeaderboardService, PointsService

# Get leaderboard
leaderboards = LeaderboardService.get_leaderboard('all_time')

# Get trainee's rank
rank = LeaderboardService.get_trainee_rank(trainee, 'all_time')

# Get trainee stats
points = PointsService.get_trainee_points(trainee)
win_rate = PointsService.get_trainee_win_rate(trainee)
progress = PointsService.get_progress_percentage(trainee)
next_belt = PointsService.get_next_belt_threshold(trainee)
```

## Example Scenarios

### Scenario 1: New Trainee (White Belt)

```
1. Trainee registers
2. TraineePoints created automatically (0 points)
3. Trainee in white belt (0 points required)
4. Participates in first event:
   - Wins: gets 30 points
   - Now: 30/150 points to yellow belt
5. View progress at /trainee/<id>/points/
```

### Scenario 2: Promotion

```
1. Blue belt trainee has 870 points (need 900 for brown)
2. Wins 3 matches in one event:
   - +30, +30, +30 = +90 points
   - Total: 960 points
3. check_belt_rank_promotion() executes
4. Trainee promoted to brown belt
5. BeltRankProgress created with timestamp
6. Leaderboards updated
7. Trainee can see promotion in profile history
```

### Scenario 3: Viewing Leaderboard

```
Judge views /leaderboard/all-time/:
- Sees top 50 trainees ranked by total points
- Sees medals for top 3 (🥇🥈🥉)
- Can filter by belt rank
- Can click trainee name to see full profile
```

## Customizing the System

### Change Point Values

Edit `core/models.py` TraineePoints class:

```python
def add_win(self):
    """Add points for a win (CHANGE THIS)."""
    self.total_points += 50  # Changed from 30
    self.wins += 1
    self.save()
    self.check_belt_rank_promotion()

def add_loss(self):
    """Add points for a loss (CHANGE THIS)."""
    self.total_points += 15  # Changed from 10
    self.losses += 1
    self.save()
    self.check_belt_rank_promotion()
```

Then migrate (no database change needed):
```bash
python manage.py makemigrations
python manage.py migrate
```

### Change Belt Thresholds

Via Django admin:
1. Go to `/admin/core/beltrankthreshold/`
2. Edit point values for each belt
3. Save changes

Or programmatically:
```python
from core.models import BeltRankThreshold

# Update brown belt to 1500 points
BeltRankThreshold.objects.filter(belt_rank='brown').update(points_required=1500)
```

### Add New Belt (Advanced)

1. Update `Trainee.BELT_CHOICES` in `core/models.py`
2. Add migrations
3. Add threshold via admin or command
4. Create management command

## Testing Points System

### Manual Testing

1. **Create test event and matches**
   - Admin creates event
   - Adds 2 trainees as competitors
   - Creates matches

2. **Submit results**
   - Judge logs in
   - Views assigned matches
   - Submits result (marks winner)

3. **Check points awarded**
   - Go to `/admin/core/trainepoints/`
   - Verify winner has +30 points
   - Verify loser has +10 points

4. **Check leaderboards**
   - Go to `/leaderboard/all-time/`
   - Should see trainees ranked by points
   - Ranks should update automatically

5. **Check promotions**
   - Submit enough matches to reach threshold
   - Check trainee's profile at `/trainee/<id>/points/`
   - Promotion should be visible in history

### Automated Testing

```python
from core.models import MatchResult, TraineePoints

# Create match result
result = MatchResult.objects.create(
    match=match,
    judge=judge,
    winner=trainee1,
    competitor1_score=10,
    competitor2_score=5,
    is_locked=True
)

# Check points were awarded
trainee1_points = TraineePoints.objects.get(trainee=trainee1)
assert trainee1_points.total_points == 30
assert trainee1_points.wins == 1
```

## Troubleshooting Integration

### Points Not Awarded

Check:
1. MatchResult saved (not deleted)
2. `_award_match_points()` is in MatchResult.save()
3. TraineePoints records exist
4. No exceptions in logs

### Leaderboard Empty

Check:
1. TraineePoints exist
2. Leaderboard.update_all_leaderboards() called
3. Year/month parameters correct

### Promotions Not Happening

Check:
1. Points are being awarded
2. Points meet threshold
3. BeltRankThreshold exists
4. No exceptions in logs

## Performance Tips

1. **Caching**: Cache leaderboard queries if high traffic
   ```python
   from django.views.decorators.cache import cache_page
   
   @cache_page(60 * 5)  # Cache for 5 minutes
   def leaderboard_all_time(request):
       ...
   ```

2. **Batch Updates**: Update leaderboards in background task
   ```python
   # Use Celery or similar for heavy operations
   @task
   def update_leaderboards():
       LeaderboardService.update_all_leaderboards()
   ```

3. **Database Indexes**: Already in place on ForeignKeys

## Files Reference

### Core Models
- `core/models.py` - BeltRankThreshold, TraineePoints, BeltRankProgress, Leaderboard

### Views
- `core/views/leaderboard.py` - All leaderboard views

### Services
- `core/services/leaderboard_service.py` - Business logic

### Templates
- `templates/leaderboard/*.html` - Display templates

### Admin
- `core/admin.py` - Admin registration

### Management Commands
- `core/management/commands/initialize_belt_thresholds.py`

### Documentation
- `BELT_RANK_AND_LEADERBOARD_GUIDE.md` - Complete reference
- `LEADERBOARD_IMPLEMENTATION_SUMMARY.md` - Features overview
- `INTEGRATION_GUIDE_LEADERBOARD.md` - This file

## What's Next?

### To Use the System:
1. ✅ Migrations applied
2. ✅ Thresholds initialized
3. ✅ Views created
4. ✅ Admin registered
5. Go to `/leaderboard/all-time/` to view rankings
6. Submit match results as judge
7. Watch points and rankings update automatically

### To Add More Features:
- See Future Enhancements in BELT_RANK_AND_LEADERBOARD_GUIDE.md
- Add seasonal leaderboards
- Add category filters
- Add charts and analytics

## Support Resources

1. **Full Documentation**: `BELT_RANK_AND_LEADERBOARD_GUIDE.md`
2. **Quick Summary**: `LEADERBOARD_IMPLEMENTATION_SUMMARY.md`
3. **Code Comments**: See docstrings in models.py and views
4. **Admin Interface**: Manage data at `/admin/`

The system is **production-ready** and automatically handles all point allocation and promotion logic!

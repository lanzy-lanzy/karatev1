# Belt Rank and Leaderboard System Guide

## Overview

The Belt Rank and Leaderboard system tracks trainee progress through points earned in events and matches. The system automatically promotes trainees to higher belt ranks based on accumulated points.

## System Components

### 1. Models

#### BeltRankThreshold
Defines the points required for each belt rank level.

```python
BeltRankThreshold
- belt_rank: CharField (white, yellow, orange, green, blue, brown, black)
- points_required: IntegerField (0, 150, 350, 600, 900, 1300, 1800)
- description: TextField
```

**Default Thresholds:**
- White Belt: 0 points (starting rank)
- Yellow Belt: 150 points
- Orange Belt: 350 points
- Green Belt: 600 points
- Blue Belt: 900 points
- Brown Belt: 1,300 points
- Black Belt: 1,800 points

#### TraineePoints
Tracks points earned by trainees through event participation.

```python
TraineePoints
- trainee: OneToOneField(Trainee)
- total_points: IntegerField (default: 0)
- wins: IntegerField (default: 0)
- losses: IntegerField (default: 0)
- events_participated: IntegerField (default: 0)
- updated_at: DateTimeField (auto_now)

Methods:
- add_win(): Add 30 points for a win
- add_loss(): Add 10 points for a loss
- check_belt_rank_promotion(): Check and apply automatic promotions
```

#### BeltRankProgress
Tracks all belt rank promotions for a trainee.

```python
BeltRankProgress
- trainee: ForeignKey(Trainee)
- old_belt_rank: CharField
- new_belt_rank: CharField
- points_earned: IntegerField
- promoted_at: DateTimeField (auto_now_add)
```

#### Leaderboard
Maintains ranking data for different timeframes.

```python
Leaderboard
- trainee: ForeignKey(Trainee)
- rank: IntegerField
- points: IntegerField
- timeframe: CharField (all_time, yearly, monthly)
- belt_rank: CharField
- year: IntegerField (nullable)
- month: IntegerField (nullable)
- updated_at: DateTimeField (auto_now)

Timeframes:
- all_time: Overall rankings across all time
- yearly: Rankings for a specific year
- monthly: Rankings for a specific month/year
```

### 2. Points System

#### How Points Are Awarded

Points are automatically awarded when match results are recorded:

1. **Win in Event:** +30 points
2. **Loss in Event:** +10 points (participation points)

#### Points Flow

```
Match Completed
    ↓
Result Submitted by Judge
    ↓
MatchResult.save() triggered
    ↓
_award_match_points() called
    ↓
├─ Winner: add_win() → +30 points
├─ Loser: add_loss() → +10 points
│
└─ Automatic Promotion Check
   ├─ Reached next threshold?
   ├─ Promote trainee
   └─ Create BeltRankProgress record
```

### 3. Belt Rank Promotions

#### Automatic Promotion Process

When a trainee's points reach the threshold for the next belt rank:

1. System detects threshold reached
2. Trainee's belt rank is automatically updated
3. BeltRankProgress entry is created
4. Trainee can view promotion in their profile

#### Promotion History

Trainees can view their complete promotion history showing:
- Previous belt rank
- New belt rank
- Points earned at promotion
- Promotion date and time

### 4. Leaderboard System

#### Leaderboard Types

1. **All-Time Leaderboard**
   - Overall rankings across entire system
   - Never resets
   - Updated after each match result

2. **Yearly Leaderboard**
   - Rankings for a specific calendar year
   - Resets annually
   - Filtered by match dates

3. **Monthly Leaderboard**
   - Rankings for a specific month/year
   - Resets monthly
   - Filtered by match dates

#### Filtering Options

- Filter by belt rank: View top trainees in each belt level
- View individual trainee profiles with progress bars
- See win/loss statistics

### 5. Views and URLs

#### Leaderboard Views

```
/leaderboard/all-time/
  GET - Display all-time leaderboard

/leaderboard/yearly/?year=2024
  GET - Display yearly leaderboard
  - year parameter: Specify year (default: current year)

/leaderboard/monthly/?year=2024&month=11
  GET - Display monthly leaderboard
  - year parameter: Specify year (default: current year)
  - month parameter: Specify month (default: current month)

/leaderboard/by-belt/?belt=blue&timeframe=all_time
  GET - Display leaderboard filtered by belt rank
  - belt parameter: Belt rank (white, yellow, orange, etc.)
  - timeframe parameter: Leaderboard timeframe

/trainee/<trainee_id>/points/
  GET - View trainee's points and belt progress
  - Shows total points, wins, losses
  - Displays progress towards next belt rank
  - Shows complete promotion history

/belt-rank/progress/
  GET - View belt rank system overview
  - Shows all belt thresholds
  - Recent promotions
  - System explanation
```

#### Leaderboard Columns

- **Rank**: Position in leaderboard (with medals for top 3)
- **Trainee Name**: Full name of trainee
- **Belt Rank**: Current belt rank with visual indicator
- **Points**: Total points earned
- **Action**: View trainee profile link

### 6. Services

#### LeaderboardService

Utility functions for leaderboard operations:

```python
LeaderboardService.update_all_leaderboards()
  - Update all timeframe leaderboards

LeaderboardService.update_leaderboard(timeframe, year, month)
  - Update specific timeframe leaderboard
  - Parameters:
    - timeframe: 'all_time', 'yearly', or 'monthly'
    - year: Year for yearly/monthly (optional)
    - month: Month for monthly (optional)

LeaderboardService.get_leaderboard(timeframe, year, month, belt_rank)
  - Retrieve leaderboard entries
  - Returns QuerySet of Leaderboard objects

LeaderboardService.get_trainee_rank(trainee, timeframe, year, month)
  - Get specific trainee's leaderboard entry
  - Returns Leaderboard object or None
```

#### PointsService

Utility functions for points operations:

```python
PointsService.add_match_result_points(match_result)
  - Award points based on match result
  - Called automatically when result is saved

PointsService.get_trainee_points(trainee)
  - Get or create TraineePoints record
  - Returns TraineePoints instance

PointsService.get_trainee_win_rate(trainee)
  - Calculate win rate percentage
  - Returns float (0-100)

PointsService.get_next_belt_threshold(trainee)
  - Get next belt rank requirement
  - Returns BeltRankThreshold or None

PointsService.get_progress_percentage(trainee)
  - Calculate progress towards next belt
  - Returns float (0-100)
```

### 7. Admin Interface

All new models are registered in Django admin:

- **BeltRankThreshold**: View and edit belt rank point requirements
- **TraineePoints**: View trainee points and stats
- **BeltRankProgress**: View promotion history
- **Leaderboard**: View and manage leaderboard rankings

## Data Flow Examples

### Example 1: Match Result Recording

```
Judge submits match result:
  Competitor1 (Blue Belt) vs Competitor2 (Blue Belt)
  Winner: Competitor1

1. MatchResult record created
2. _award_match_points() executes:
   - Competitor1 points: 50 → 80 (add_win: +30)
   - Competitor2 points: 850 → 860 (add_loss: +10)
3. Competitor2 points check:
   - 860 >= 900? No → No promotion
4. Leaderboards updated:
   - All-time, yearly, and monthly rankings recalculated
```

### Example 2: Belt Promotion

```
Trainee at 870 points, Blue Belt

Wins a match: +30 points
Trainee now has 900 points

check_belt_rank_promotion() executes:
1. Current belt: blue (index 4)
2. Next belt: brown (index 5)
3. Brown threshold: 1300 points
4. 900 >= 1300? No → No promotion

Later, after several more wins:
Trainee reaches 1300 points

1. Current belt: blue
2. Next belt: brown
3. Brown threshold: 1300 points
4. 1300 >= 1300? Yes → PROMOTION!
5. Update trainee.belt_rank = 'brown'
6. Create BeltRankProgress:
   - old_belt_rank: 'blue'
   - new_belt_rank: 'brown'
   - points_earned: 1300
7. Trainee can see promotion in profile
```

## Management Commands

### Initialize Belt Thresholds

```bash
python manage.py initialize_belt_thresholds
```

Populates BeltRankThreshold with default values:
- White: 0 points
- Yellow: 150 points
- Orange: 350 points
- Green: 600 points
- Blue: 900 points
- Brown: 1300 points
- Black: 1800 points

## Configuration

### Customizing Point Values

Edit point values in MatchResult model or service:

```python
# In TraineePoints.add_win()
self.total_points += 30  # Change to desired value

# In TraineePoints.add_loss()
self.total_points += 10  # Change to desired value
```

### Customizing Belt Thresholds

Update BeltRankThreshold model values in admin or via management command:

```python
BeltRankThreshold.objects.filter(belt_rank='brown').update(points_required=1500)
```

## Display Elements

### Leaderboard Table

Shows ranked list of trainees with:
- Rank number with medal (🥇🥈🥉)
- Trainee name
- Belt rank badge (color-coded)
- Total points
- Link to trainee profile

### Progress Bar

Displays visual progress towards next belt rank:
- Shows current points / required points
- Percentage filled based on progress
- Color-coded (green for progress)

### Statistics Cards

Trainee profile displays:
- Total points
- Number of wins
- Number of losses
- Events participated
- Last update timestamp

## API Integration

### Getting Leaderboard Data in Views

```python
from core.services.leaderboard_service import LeaderboardService

# Get all-time leaderboard
leaderboards = LeaderboardService.get_leaderboard('all_time')

# Get specific trainee's rank
trainee_entry = LeaderboardService.get_trainee_rank(trainee, 'all_time')
rank = trainee_entry.rank if trainee_entry else None

# Get trainee stats
from core.services.leaderboard_service import PointsService

points = PointsService.get_trainee_points(trainee)
win_rate = PointsService.get_trainee_win_rate(trainee)
progress = PointsService.get_progress_percentage(trainee)
next_belt = PointsService.get_next_belt_threshold(trainee)
```

## Performance Considerations

1. **Leaderboard Updates**: Triggered after each match result
2. **Index Optimization**: Foreign keys and frequently filtered fields are indexed
3. **Caching**: Consider caching leaderboard queries for high-traffic scenarios
4. **Batch Operations**: Use bulk_create for large-scale updates

## Future Enhancements

1. **Seasonal Leaderboards**: Quarter-based rankings
2. **Category Leaderboards**: Separate rankings by weight class
3. **Streak Tracking**: Track win/loss streaks
4. **Performance Stats**: Advanced statistics and analytics
5. **Notifications**: Alert trainees on promotions
6. **Historical Charts**: Visualize point progression over time
7. **Export Data**: CSV/PDF export of leaderboards

## Troubleshooting

### Trainee Not Getting Promoted

Check:
1. Match result was properly saved
2. Points were awarded (check TraineePoints record)
3. Points meet threshold (check BeltRankThreshold)
4. No exceptions in point checking logic

### Leaderboard Not Updating

Check:
1. Leaderboard.update_all_leaderboards() was called
2. TraineePoints records exist for trainees
3. Year/month parameters match if filtering by timeframe

### Wrong Points Value

Check:
1. MatchResult.save() is calling _award_match_points()
2. TraineePoints.add_win() and add_loss() have correct values
3. No duplicate point awards

## Support

For issues or questions about the belt rank and leaderboard system:
1. Check this guide
2. Review admin interface for data consistency
3. Check Django logs for exceptions
4. Verify migration was applied successfully

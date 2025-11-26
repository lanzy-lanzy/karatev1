# Belt Rank & Leaderboard System - Quick Reference

## What's New?

### Dashboard Stats (4 Cards)
```
┌─────────┬───────┬────────┬──────────────┐
│ Points  │ Wins  │ Losses │ Leaderboard  │
│  (Blue) │(Green)│(Orange)│  Rank(Purple)│
└─────────┴───────┴────────┴──────────────┘
```

### Belt Progress
```
Current: Blue Belt → Next: Brown Belt
Points: 870 / 900
Progress Bar: ████████░ 96.7%
Message: "Keep Going! 30 more points needed"
```

## Quick Links

| Page | URL | Purpose |
|------|-----|---------|
| Dashboard | `/trainee/dashboard/` | View stats & progress |
| Leaderboard | `/leaderboard/all-time/` | All-time rankings |
| Yearly | `/leaderboard/yearly/` | Year rankings |
| Monthly | `/leaderboard/monthly/` | Month rankings |
| By Belt | `/leaderboard/by-belt/` | Filter by belt rank |
| Profile | `/trainee/<id>/points/` | Individual stats |
| System | `/belt-rank/progress/` | Belt info & thresholds |
| Admin | `/admin/` | Manage system |

## Sidebar Menu

```
Dashboard
Upcoming Events
Schedule Match
Payments History
─────────────────
RANKINGS
  Leaderboard →
  Belt System →
```

## Points System

| Action | Points |
|--------|--------|
| Win a match | +30 |
| Lose a match | +10 |
| Participate (lose) | 10 pts |

## Belt Ranks

| Rank | Points | Color |
|------|--------|-------|
| White | 0 | Gray |
| Yellow | 150 | Yellow |
| Orange | 350 | Orange |
| Green | 600 | Green |
| Blue | 900 | Blue |
| Brown | 1300 | Brown |
| Black | 1800 | Black |

## Stat Cards Explained

### Total Points (Blue)
- Cumulative points from all matches
- 30 pts per win, 10 pts per loss
- Updates after each match

### Wins (Green)
- Number of matches won
- Shows win rate percentage
- (Wins / Total Matches) × 100

### Losses (Orange)
- Number of matches lost
- Shows total matches participated
- Wins + Losses = Total Matches

### Leaderboard Rank (Purple)
- Current rank among all trainees
- # sign (e.g., #5)
- Updates after each match
- Link to full leaderboard

## Progress Bar

- **Visual representation** of progress to next belt
- **Current points / Required points**
- **Percentage** shown below (0-100%)
- **Green gradient** indicates progress
- **Animation** when earning points

## Leaderboard Features

- **Rankings** sorted by total points
- **Belt rank** shown for each trainee
- **Medals** for top 3 (🥇🥈🥉)
- **Multiple timeframes** (all-time, yearly, monthly)
- **Filter by belt** to see specific rank levels
- **Quick links** to trainee profiles

## How It Works

### Automatic Process
```
Judge submits match result
    ↓
Points awarded automatically
    ├─ Winner: +30 pts
    └─ Loser: +10 pts
    ↓
Threshold reached?
    ├─ Yes: Promote to next belt
    └─ No: Keep going
    ↓
Leaderboards update
Dashboard refreshes
```

### No Extra Steps Required!
Just submit match results as normal.

## Admin Tasks

| Task | Location |
|------|----------|
| View belt thresholds | `/admin/core/beltrankthreshold/` |
| View trainee stats | `/admin/core/trainepoints/` |
| View promotions | `/admin/core/beltrankprogress/` |
| View rankings | `/admin/core/leaderboard/` |
| Edit thresholds | Click threshold → Edit |
| Edit stats | Click stats → Edit |

## Customize (Advanced)

### Change Win Points
File: `core/models.py`
```python
def add_win(self):
    self.total_points += 30  # Change this number
```

### Change Loss Points
File: `core/models.py`
```python
def add_loss(self):
    self.total_points += 10  # Change this number
```

### Change Belt Thresholds
Admin: `/admin/core/beltrankthreshold/`
- Edit each belt's `points_required` field

## Stats Definitions

| Stat | Formula | Example |
|------|---------|---------|
| Total Points | Sum of all match points | 450 |
| Wins | Count of won matches | 12 |
| Losses | Count of lost matches | 8 |
| Win Rate | (Wins / Total) × 100 | 60% |
| Progress % | (Current / Required) × 100 | 85% |
| Rank | Position in leaderboard | #5 |
| Points Needed | Required - Current | 50 |

## Colors

| Color | Represents |
|-------|------------|
| Blue | Points/Achievement |
| Green | Wins/Success |
| Orange | Losses/Caution |
| Purple | Ranking/Position |
| Yellow | Alert/Maximum |

## Shortcuts

### For Trainee
- Dashboard → See stats
- Leaderboard → Compare scores
- Belt System → Learn thresholds
- Submit match result (as judge) → Auto-update

### For Admin
- Admin → `/admin/`
- Thresholds → `/admin/core/beltrankthreshold/`
- Stats → `/admin/core/trainepoints/`

## FAQ

**Q: When do points update?**  
A: When judge submits match result.

**Q: When do I get promoted?**  
A: When points reach next belt threshold (automatic).

**Q: Can I lose points?**  
A: No, only gain (30 for win, 10 for loss).

**Q: Who can see leaderboards?**  
A: Any logged-in user (trainee, judge, admin).

**Q: Can thresholds be changed?**  
A: Yes, via `/admin/core/beltrankthreshold/`

**Q: How often updates?**  
A: Immediately after each match result.

**Q: Mobile friendly?**  
A: Yes, fully responsive.

**Q: Can I undo a promotion?**  
A: No, promotions are permanent (by design).

## Setup Commands

```bash
# Apply database changes
python manage.py migrate

# Initialize belt thresholds
python manage.py initialize_belt_thresholds

# Create superuser (if needed)
python manage.py createsuperuser

# Run server
python manage.py runserver
```

## File Locations

```
Views:     core/views/leaderboard.py
           core/views/trainee.py (updated)
Templates: templates/leaderboard/
           templates/trainee/dashboard.html (updated)
Models:    core/models.py (4 new models)
Services:  core/services/leaderboard_service.py
Admin:     core/admin.py
URLs:      core/urls.py
Migrations: core/migrations/
```

## Getting Help

| Question | Document |
|----------|----------|
| How do I use it? | LEADERBOARD_QUICK_START.md |
| What's new? | DASHBOARD_INTEGRATION_COMPLETE.md |
| Full details? | BELT_RANK_AND_LEADERBOARD_GUIDE.md |
| How's it built? | IMPLEMENTATION_COMPLETE_LEADERBOARD.md |
| Complete list? | IMPLEMENTATION_FINAL_CHECKLIST.md |
| Overview? | FINAL_IMPLEMENTATION_SUMMARY.md |

## Key Numbers

- **7** belt ranks (White to Black)
- **1,800** maximum points (Black Belt)
- **30** points for win
- **10** points for loss
- **4** stat cards on dashboard
- **6** leaderboard endpoints
- **3** timeframe options (all-time, yearly, monthly)
- **0%** chance of manual intervention (all automatic!)

---

**Print this page for quick reference!**

Version 1.0 | November 26, 2025 | Status: ✅ Production Ready

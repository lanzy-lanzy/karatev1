# Populate Leaderboard Data

## Quick Start

To populate the leaderboard with test data and see it in action:

```bash
# Activate virtual environment (if not already active)
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Run the population command
python manage.py populate_leaderboard_data
```

## What This Does

The command will:

1. **Create 10 Additional Test Trainees** with different belt ranks:
   - White belt: John Karate, James Swift
   - Yellow belt: Sarah Warrior, Emma Tiger
   - Orange belt: Mike Champion
   - Green belt: Anna Dragon, Robert Phoenix
   - Blue belt: Alex Thunder
   - Brown belt: David Master
   - Black belt: Lisa Ninja

2. **Create a Spring Tournament 2025 Event**
   - Scheduled for 30 days from now
   - Registration deadline in 20 days
   - Max participants: 50

3. **Register All Trainees** to the event

4. **Create Matches** between pairs of trainees:
   - 5-6 matches depending on total trainee count
   - Random opponent selection
   - Scheduled 25 days from now

5. **Generate Match Results**:
   - Randomly determine winners
   - Award points (30 for win, 10 for loss)
   - Automatically promote belt ranks based on points

6. **Update Leaderboards**:
   - All-time rankings
   - Yearly rankings
   - Monthly rankings

## Viewing the Leaderboard

After running the command:

1. Start the development server:
   ```bash
   python manage.py runserver
   ```

2. Visit the leaderboard pages:
   - **All Time**: `http://localhost:8000/leaderboard/all-time/`
   - **Yearly**: `http://localhost:8000/leaderboard/yearly/`
   - **Monthly**: `http://localhost:8000/leaderboard/monthly/`

3. You should see:
   - ✅ 10+ trainees ranked by points
   - ✅ Medal indicators (🥇 🥈 🥉) for top 3
   - ✅ Belt rank badges with colors
   - ✅ Points progression bars
   - ✅ Profile links to view individual trainee stats

## Data Details

### Trainees Created:
| Username | Name | Belt | Weight | Points |
|----------|------|------|--------|--------|
| trainee_john | John Karate | White | 70.5 kg | Varies |
| trainee_sarah | Sarah Warrior | Yellow | 65.0 kg | Varies |
| trainee_mike | Mike Champion | Orange | 85.5 kg | Varies |
| trainee_anna | Anna Dragon | Green | 60.0 kg | Varies |
| trainee_alex | Alex Thunder | Blue | 78.5 kg | Varies |
| trainee_david | David Master | Brown | 82.0 kg | Varies |
| trainee_lisa | Lisa Ninja | Black | 58.5 kg | Varies |
| trainee_james | James Swift | White | 72.0 kg | Varies |
| trainee_emma | Emma Tiger | Yellow | 62.5 kg | Varies |
| trainee_robert | Robert Phoenix | Green | 88.0 kg | Varies |

### Default Credentials:
- **Username**: Any of the above
- **Password**: `TestPassword123!`

### Points System:
- Win in event: +30 points
- Loss in event: +10 points

## Features of the Enhanced Leaderboard

### Visual Design
- ✨ Modern gradient headers
- 🏆 Medal icons for top 3 ranks
- 🎯 Color-coded belt rank badges
- 📊 Points progress bars
- 🎨 Responsive grid layout

### Functionality
- 🔄 Filter by timeframe (All Time, Yearly, Monthly)
- 👤 View individual trainee profiles
- 📈 See points and rankings
- 🎪 Animated hover effects
- 📱 Mobile responsive design

### Data Displayed
- Trainee rank and name
- Current belt rank
- Total points earned
- Visual progress bar
- Quick profile access

## Resetting Data

To clear and repopulate:

```bash
# Option 1: Just clear leaderboard and recreate
python manage.py populate_leaderboard_data

# Option 2: Delete and recreate everything
# (requires manual database deletion first)
rm db.sqlite3
python manage.py migrate
python manage.py create_test_users
python manage.py initialize_belt_thresholds
python manage.py populate_leaderboard_data
```

## Troubleshooting

### No data shows up
- Ensure migrations are run: `python manage.py migrate`
- Check that `populate_leaderboard_data` completed successfully
- Verify trainees exist: `python manage.py shell` then `from core.models import Trainee; print(Trainee.objects.count())`

### Wrong points in leaderboard
- Points are awarded automatically when match results are recorded
- Check `TraineePoints` model: `from core.models import TraineePoints; print(TraineePoints.objects.all())`

### Trainees not appearing in leaderboard
- Ensure `Leaderboard` entries were created
- Verify belt ranks are set correctly
- Check that points calculations are working

## Next Steps

After populating:

1. **Test Admin Panel**: `http://localhost:8000/admin/` (use admin credentials)
2. **View Trainee Dashboard**: `http://localhost:8000/trainee/dashboard/` (use any trainee credentials)
3. **Check Leaderboards**: Navigate to any leaderboard view to see rankings
4. **Create More Matches**: Use admin panel to create additional matches and results

---

**Enjoy your fully populated leaderboard! 🥋**

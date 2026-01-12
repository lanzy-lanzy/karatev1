# Belt Scoring & Admin Evaluations Guide

## Overview
The admin evaluation form now includes a dedicated **Belt Rank Scoring** section where you can input numeric scores (0-100) for four key categories. These scores automatically calculate belt points that contribute to trainee belt rank progression.

## How It Works

### 1. Belt Scoring Section
Located at the top of the admin evaluation form, this section includes four input fields:

#### Score Categories & Weights:
- **Attendance Score (10% weight)** - Rate trainee's attendance/reliability (0-100)
- **Sparring Score (20% weight)** - Rate sparring/combat performance (0-100)
- **Achievement Score (10% weight)** - Rate accomplishments/goals (0-100)
- **Performance Score (10% weight)** - Rate overall performance (0-100)

### 2. Automatic Calculation
As you enter scores, the **Total Belt Points** displays automatically at the bottom of the Belt Scoring section.

**Formula:**
```
Total Belt Points = (Attendance × 0.10) + (Sparring × 0.20) + (Achievement × 0.10) + (Performance × 0.10)
```

**Example:**
```
Attendance: 85
Sparring: 90
Achievement: 80
Performance: 88

Total = (85 × 0.10) + (90 × 0.20) + (80 × 0.10) + (88 × 0.10)
      = 8.5 + 18.0 + 8.0 + 8.8
      = 43 points
```

### 3. Creating an Evaluation

**Step 1:** Go to Admin → Evaluations → New Evaluation

**Step 2:** Select a trainee from the dropdown

**Step 3:** In the **Belt Rank Scoring** section (blue box at top):
- Enter Attendance Score: `0-100`
- Enter Sparring Score: `0-100`
- Enter Achievement Score: `0-100`
- Enter Performance Score: `0-100`

**Step 4:** Watch the Total Belt Points calculate automatically

**Step 5:** (Optional) Fill in the Performance Ratings section below for additional feedback

**Step 6:** (Optional) Add detailed comments, strengths, and recommendations

**Step 7:** Click "Create Evaluation"

### 4. Trainee Dashboard Display
Once an evaluation is created:

1. The trainee will see a **"Recent Evaluations"** section on their dashboard
2. The table shows:
   - **Date** - When the evaluation was created
   - **Attendance Score** - The score you entered
   - **Sparring Score** - The score you entered
   - **Achievement Score** - The score you entered
   - **Performance Score** - The score you entered
   - **Total Points Earned** - The calculated belt points (+X)

### 5. Example Table in Trainee Dashboard

```
Date          | Attendance | Sparring | Achievement | Performance | Total Points
Jan 12, 2026  |    85      |    90    |     80      |     88      |     +43
Jan 05, 2026  |    80      |    85    |     78      |     82      |     +40
```

### 6. Editing an Evaluation

If you need to update scores:
1. Go to Admin → Evaluations
2. Find the evaluation and click "Edit"
3. Update any Belt Scoring fields
4. The Total Belt Points will recalculate
5. Click "Update Evaluation"

## Key Features

✓ **Real-time calculation** - Points update as you type
✓ **Weighted scoring** - Sparring counts 2x more than other categories
✓ **Trainee visibility** - Trainees see exact breakdown of their scoring
✓ **Historical tracking** - All evaluations stored with detailed breakdown
✓ **Belt progression** - Points contribute to trainee's belt rank advancement

## Notes

- Scores must be between 0-100
- All four score fields are required
- Total Belt Points are rounded to nearest integer
- Performance Ratings section remains optional for backward compatibility
- Evaluations are marked as "completed" upon creation

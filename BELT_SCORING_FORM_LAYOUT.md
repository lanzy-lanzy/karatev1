# Belt Scoring Evaluation Form - Layout Guide

## Complete Form Structure

### URL
```
Admin: /admin/evaluations/add/
Edit:  /admin/evaluations/<id>/edit/
```

---

## Form Sections (Top to Bottom)

### 1. TRAINEE SELECTION
```
┌─────────────────────────────────────────────────────────────┐
│ Select Trainee                                              │
│ ┌───────────────────────────────────────────────────────┐   │
│ │ -- Select a trainee --                          ▼    │   │
│ │ John Doe (Green Belt)                                 │   │
│ │ Sarah Johnson (Yellow Belt)                          │   │
│ │ Mike Smith (Blue Belt)                              │   │
│ └───────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

### 2. BELT RANK SCORING (NEW - BLUE SECTION)
```
┌──────────────────────────────────────────────────────────────┐
│ ■■■ Belt Rank Scoring (Blue highlighted box)                │
│ Enter scores (0-100) for each category. These points         │
│ contribute to trainee's belt rank progression.               │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Attendance Score (10% weight) │ Sparring Score (20% weight) │
│  ┌─────────────────────────┐   │ ┌─────────────────────────┐ │
│  │ [______] 0-100          │   │ │ [______] 0-100          │ │
│  └─────────────────────────┘   │ └─────────────────────────┘ │
│                                 │                              │
│  Achievement Score (10% weight) │ Performance Score (10% wt)  │
│  ┌─────────────────────────┐   │ ┌─────────────────────────┐ │
│  │ [______] 0-100          │   │ │ [______] 0-100          │ │
│  └─────────────────────────┘   │ └─────────────────────────┘ │
│                                                               │
├──────────────────────────────────────────────────────────────┤
│ Total Belt Points (calculated automatically)                 │
│ ╔══════════════════════════════════════════════════════════╗ │
│ ║                                                          43║ │
│ ╚══════════════════════════════════════════════════════════╝ │
└──────────────────────────────────────────────────────────────┘
```

---

### 3. PERFORMANCE RATINGS (OPTIONAL - GRAY SECTION)
```
┌──────────────────────────────────────────────────────────────┐
│ Performance Ratings (Optional)                               │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Technique              │  Speed                             │
│  ┌──────────────────┐   │  ┌──────────────────┐             │
│  │ Poor        ▼    │   │  │ Poor        ▼    │             │
│  └──────────────────┘   │  └──────────────────┘             │
│                         │                                    │
│  Strength               │  Flexibility                       │
│  ┌──────────────────┐   │  ┌──────────────────┐             │
│  │ Poor        ▼    │   │  │ Poor        ▼    │             │
│  └──────────────────┘   │  └──────────────────┘             │
│                         │                                    │
│  Discipline             │  Fighting Spirit                   │
│  ┌──────────────────┐   │  ┌──────────────────┐             │
│  │ Poor        ▼    │   │  │ Poor        ▼    │             │
│  └──────────────────┘   │  └──────────────────┘             │
│                                                               │
│  Overall Rating                                              │
│  ┌──────────────────┐                                        │
│  │ Poor        ▼    │                                        │
│  └──────────────────┘                                        │
└──────────────────────────────────────────────────────────────┘
```

---

### 4. DETAILED ASSESSMENT
```
┌──────────────────────────────────────────────────────────────┐
│ Detailed Assessment                                          │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│ Comments                                                     │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ General comments about the trainee's performance...    │ │
│ │                                                        │ │
│ │                                                        │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                               │
│ Key Strengths                                                │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ List the trainee's strengths...                       │ │
│ │                                                        │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                               │
│ Areas for Improvement                                        │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Areas that need improvement...                       │ │
│ │                                                        │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                               │
│ Training Recommendations                                     │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Specific recommendations for training...             │ │
│ │                                                        │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                               │
│ Next Evaluation Date (Optional)                              │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ 2026-02-12                                             │ │
│ └──────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

---

### 5. FORM ACTIONS
```
┌──────────────────────────────────────────────────────────────┐
│                                                               │
│ [Create Evaluation]    [Cancel]                              │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## Key Differences

### OLD FORM (Before)
- Only rating dropdowns (Poor, Fair, Good, Excellent)
- No clear belt point calculation
- No numeric scores visible to trainees

### NEW FORM (Now)
- **NEW:** Belt Rank Scoring section with numeric fields
- **NEW:** Real-time points calculation
- **NEW:** Clear weights shown (10%, 20%, etc.)
- **KEPT:** Optional performance ratings for backward compatibility
- **KEPT:** Comments and recommendations section

---

## Input Validation

### Belt Scoring Fields
- **Required:** Yes
- **Type:** Number
- **Min:** 0
- **Max:** 100
- **Default:** 0

### Calculation
- Automatically triggers as you type
- Updates Total Belt Points in real-time
- No need to click calculate button

---

## Form Appearance

### Colors & Styling
```
Belt Rank Scoring Section:
  Background: Blue gradient (from-blue-900 to-blue-800)
  Border: Blue (#3b82f6)
  Text: White
  
Total Points Display:
  Background: Dark gray (#1f2937)
  Text: Large, bold, blue (#60a5fa)
  
Overall Form:
  Background: Dark gray (#1f2937)
  Inputs: Dark gray (#111827)
  Text: Light gray
```

---

## Live Example

When you enter:
```
Attendance: 85
Sparring: 90
Achievement: 80
Performance: 88
```

The form shows:
```
Total Belt Points (calculated automatically)
43
```

And it updates instantly as you change any number!

---

## On Mobile

Form adapts to single column:
```
Attendance Score (10%)      Sparring Score (20%)
[______] 0-100              [______] 0-100

Achievement Score (10%)     Performance Score (10%)
[______] 0-100              [______] 0-100
```

On very small screens:
```
Attendance Score (10%)
[__________] 0-100

Sparring Score (20%)
[__________] 0-100

Achievement Score (10%)
[__________] 0-100

Performance Score (10%)
[__________] 0-100
```

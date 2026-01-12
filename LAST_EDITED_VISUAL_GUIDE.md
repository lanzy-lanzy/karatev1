# Last Edited Feature - Visual Guide

## Desktop View

### Table Header
```
NAME | BELT RANK | AGE | WEIGHT CLASS | STATUS | LAST EDITED | ACTIONS
```

### Example Rows
```
Alex Thunder    | Brown | -1 | Middleweight | Active | 2 minutes ago  | Edit | Archive
Alex Yellow1    | Brown | 22 | Welterweight | Active | 1 hour ago    | Edit | Archive
Anna Dragon     | Green |    | Lightweight  | Active | 3 days ago    | Edit | Archive
Anna Orange2    | Brown | 29 | Light Heavy. | Active | 5 seconds ago | Edit | Archive
```

### Hover Effect
When you hover over a "Last Edited" cell, a tooltip appears showing the exact timestamp:
```
2 minutes ago ← Hover over this
↓
Tooltip: "2026-01-11 14:30:45"
```

## Mobile View

### Card Layout
```
┌─────────────────────────────────────────┐
│ [Avatar] Name              [Status]     │
│          email@example.com              │
│                                         │
│ Belt: Brown | Age: 22                   │
│ Weight: Welt | Last Edited: 1 hour ago  │
│                                         │
│                      [Edit] [Archive]   │
└─────────────────────────────────────────┘
```

## Time Format Examples

### Relative Timestamps
- Just now → "0 minutes ago"
- 1 minute → "1 minute ago"
- 5 minutes → "5 minutes ago"
- 1 hour → "1 hour ago"
- 2 hours → "2 hours ago"
- 1 day → "1 day ago"
- 5 days → "5 days ago"
- 1 week → "1 week ago"

### Exact Timestamp (on hover)
- Format: YYYY-MM-DD HH:MM:SS
- Example: "2026-01-11 14:30:45"
- Timezone: Uses server timezone

## Implementation Details

### Active Trainees Page
- Path: `/admin/trainees/`
- Shows all non-archived trainees
- New column displays last update time
- Updates in real-time after editing

### Archived Trainees Page
- Path: `/admin/trainees/archived/`
- Shows archived trainees
- Same "Last Edited" functionality
- Useful for tracking when trainees were archived

## Update Triggers

The "Last Edited" timestamp updates whenever:

1. **Edit Form Submission**
   - User edits trainee info via Edit button
   - Saves any field changes

2. **Direct Model Updates**
   - Administrative updates
   - Bulk operations
   - System updates

3. **What Counts as an Edit**
   - Any field modification (name, belt, weight, etc.)
   - Even if the value doesn't actually change
   - Auto-saves on every POST request to edit view

## Color Styling

### Desktop Table
- Column header: Gray text on dark background
- Cell content: Light gray text (`text-gray-400`)
- Maintains consistency with existing design

### Mobile Card
- Label: Smaller gray text
- Value: White bold text
- Tooltip: Shows on long-press on mobile

## Responsive Behavior

### Desktop (md and up)
- Full table view
- All 7 columns visible
- Last Edited column in fixed position

### Mobile (below md)
- Card view
- 2-column grid layout (was 3 columns)
- Last Edited in bottom-right of info grid
- Full timestamp visible in card

## Performance Notes

- No additional database queries
- Uses Django's built-in `auto_now` mechanism
- Humanize filter runs at template render time
- No JavaScript required for functionality

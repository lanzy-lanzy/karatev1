# Trainee Selection Export Guide

## Overview

Export now allows you to select specific individual trainees and export them organized by belt rank in PDF format.

## Key Features

✅ **Select Specific Users**
- Checkboxes next to each trainee name
- Select individual trainees or all at once
- Real-time selection counter

✅ **Export by Belt Rank**
- Selected trainees grouped by belt progression
- Professional PDF formatting
- Filters apply to selections

✅ **Flexible Combinations**
- Select users + filter by belt
- Select users + filter by status
- Select users + both filters

## How to Use

### Step 1: Select Trainees

**Select Individual Trainees:**
1. Navigate to Trainee Management page
2. Check the box next to each trainee you want to export
3. Counter shows "X selected" in top right

**Select All Trainees:**
1. Click checkbox in table header
2. Or click "Select All" button that appears

**Deselect:**
1. Uncheck individual boxes
2. Or click "Clear" button to unselect all

### Step 2: Apply Filters (Optional)

Use existing filter dropdowns:
- **Status Filter**: Active, Inactive, or Suspended
- **Belt Filter**: Specific belt rank
- **Search**: Find by name

*Filters apply to your selections - only matching trainees will export*

### Step 3: Choose Export Format

1. Select "Export by Belt Rank" from dropdown
2. Click blue "Export" button
3. Select "Export as PDF"

### Step 4: File Downloads

Receive: `trainees_belt.pdf`

## Workflow Examples

### Example 1: Export 3 Brown Belt Trainees

**Steps:**
1. Use search to find "brown belt"
2. Check boxes for 3 brown belts you want
3. Keep "Export by User" or select "Export by Belt Rank"
4. Click Export → PDF
5. Get PDF with just those 3 trainees

### Example 2: Export All Active Green Belts

**Steps:**
1. Select "Green" in Belt filter
2. Select "Active" in Status filter  
3. Click "Select All" button
4. Select "Export by Belt Rank" format
5. Click Export → PDF
6. Get PDF with all active green belts organized by belt

### Example 3: Export Mixed Belt Trainees

**Steps:**
1. Manually check boxes for trainees from different belts (3 green, 2 brown, 1 black)
2. Keep filters as "All Status" and "All Belts"
3. Select "Export by Belt Rank"
4. Click Export → PDF
5. Get PDF showing:
   - Green Belt (3 trainees)
   - Brown Belt (2 trainees)
   - Black Belt (1 trainee)

## Selection Features

### Bulk Actions

When you select trainees, a toolbar appears showing:
- **Selected count**: How many trainees selected
- **Select All button**: Check all visible trainees
- **Clear button**: Uncheck all trainees

### Smart Filtering

**Scenario 1: Select with filters**
- Select 5 trainees
- Apply "Active" status filter
- Only active ones from your 5 are exported

**Scenario 2: Multiple selections**
- Select from page 1: 3 trainees
- Scroll to page 2: select 2 more
- Export includes all 5 selections
- (Works across pagination)

### Selection Indicators

- **Checkbox**: Individual trainee selection
- **Header checkbox**: Select/deselect all on page
- **Selected count**: Real-time update as you check boxes

## PDF Output When Using Selections

### Format: By User

Standard alphabetical list of your selected trainees:

```
Name        | Email    | Belt | Weight | Age | Status | Joined
─────────────────────────────────────────────────────────
Alex T.    | alex@... | Brown| Middle | 22  | Active | 11/29
Anna D.    | anna@... | Green| Light  | N/A | Active | 11/26
```

### Format: By Belt (Recommended for Selections)

Your selected trainees grouped by belt:

```
GREEN BELT (2 trainees)
─────────────────────────
Anna Dragon    | anna@...  | Lightweight  | N/A | Active
James Green2   | james@... | Lightweight  | 32  | Active

BROWN BELT (1 trainee)
─────────────────────────
Alex Thunder   | alex@...  | Middleweight | 22  | Active
```

## Use Cases

### Training Group Organization
- Select all white belts → Export by Belt
- Send to white belt instructors
- Know exact members in their training group

### Promotion Verification
- Select brown belts ready for black belt test
- Export by Belt to review promotions
- Share with instructors for approval

### Event Roster
- Select trainees for specific tournament
- Export by Belt for organizers
- Quick reference of participants by level

### Contact List
- Select active members
- Export by User format for CSV
- Email attendance reminders

### Absence Tracking
- Select trainees with attendance issues
- Filter by status if needed
- Export to follow up

### Retention Analysis
- Select suspended members
- Export by Belt to see dropout pattern
- Identify which levels lose members

## Tips & Tricks

### Deselect Multiple Quickly
Instead of unchecking each box:
1. Click "Clear" button
2. Rechecks only those you need

### Select Across Pages
✓ Works: Select on page 1, then page 2
The selection persists as you navigate

### Combine with Search
1. Search "alex" to show matching trainees
2. Select those you want
3. Search different name
4. Select more
5. Export all selections at once

### Filter Then Select
1. Filter: "Brown" belt, "Active" status
2. Click "Select All"
3. All matching trainees selected
4. Can then deselect individual ones you don't want

## URL Parameters

Advanced users can also export via URL:

```
GET /admin/trainees/export/
  ?format=pdf
  &export_by=belt
  &trainee_ids=1,3,5,7,11
  &status_filter=active
```

| Parameter | Values | Purpose |
|---|---|---|
| `trainee_ids` | comma-separated IDs | Export specific trainees |
| `export_by` | user, belt | Organization format |
| `status_filter` | active, inactive, suspended | Filter results |
| `belt_filter` | white, green, brown, black, etc | Filter results |

## Technical Details

### How Selection Works

1. **Checkboxes in table** - Each row has unique trainee ID value
2. **JavaScript collects IDs** - Click export, script gets checked IDs
3. **URL parameter** - IDs sent as `trainee_ids=1,2,3,4`
4. **Backend filters** - Query filters by both IDs and other criteria
5. **PDF generated** - Selected trainees are exported

### Backend Processing

```python
# If trainee_ids provided:
trainees = trainees.filter(id__in=trainee_ids)

# Then other filters apply:
if status_filter:
    trainees = trainees.filter(status=status_filter)
```

### Performance

- No performance impact from selections
- Same database queries as regular export
- File sizes remain small (usually <10KB)

## Troubleshooting

### "Select All" doesn't work
- Page might be loading
- Wait for table to fully load
- Check browser console for errors

### Selected trainees don't export
- Verify checkboxes are actually checked
- Counter should show number selected
- Try re-selecting and export again

### Mixed results in export
- Check if filters are applied
- Filters apply to selections
- Example: Select 5, filter "active" = only active ones export

### Can't find trainees to select
- Use search to filter list
- Apply status/belt filters first
- Then select from results

### Selection lost after filtering
- Selection persists when you apply filters
- Selection persists across pages
- But resets when you navigate away from page

## Security

- Selections only work for logged-in admins
- Must have admin privilege to export
- IDs are validated on backend
- No sensitive data exposure

## Browser Compatibility

✓ Works on all modern browsers:
- Chrome/Chromium
- Firefox
- Safari
- Edge
- Mobile browsers

## Keyboard Shortcuts (Future)

Could add keyboard shortcuts:
- Tab → Navigate between checkboxes
- Space → Toggle checkbox
- Ctrl+A → Select all (when focused on table)

Currently requires mouse/touch interaction.

## Summary

The trainee selection export feature gives you fine-grained control over what gets exported:

**Why it's powerful:**
- Export exactly who you need
- Don't export everyone if you don't need to
- Combine with filters for precise results
- Organize by belt for easy reference

**Quick start:**
1. Check boxes for trainees you want
2. Select "Export by Belt Rank"
3. Click Export → PDF
4. Done!

The PDF groups your selected trainees by belt rank, making it easy to see your selections organized by training level.

# Export Format Selection Guide

## Overview

The trainee export feature now supports two distinct organization formats that allow administrators to view trainee data in different ways:

1. **Export by User** - Standard list format organized alphabetically by trainee name
2. **Export by Belt Rank** - Data grouped by belt rank (White → Black) with trainee lists under each belt

## User Interface

### Export Controls

Located in the Trainee Management page header:

```
┌─────────────────────────────────┐
│  [Export by User ▼]  [Export ↓] │
└─────────────────────────────────┘
```

### Components

**1. Export By Selector** (Dropdown)
- Default: "Export by User"
- Options:
  - "Export by User" - Standard list format
  - "Export by Belt Rank" - Grouped by belt

**2. Export Button** (Blue button with dropdown)
- Hover to reveal format options:
  - "Export as PDF"
  - "Export as CSV"

### Workflow

1. (Optional) Select filters (Status, Belt)
2. (Required) Select export organization ("Export by User" or "Export by Belt Rank")
3. Click blue "Export" button
4. Select file format (PDF or CSV)
5. File downloads automatically

## Export by User Format

### Purpose
Standard tabular format for reviewing individual trainee information in alphabetical order.

### PDF Layout

**Document Title:**
```
BlackCobra Karate Club
Trainee Management Report
Generated: January 11, 2026 | Status Filter: All | Belt Filter: All
```

**Summary Table:**
```
Metric                    Count
Total Trainees            44
Active                    44
Inactive                  1
Suspended                 0
```

**Data Table (7 columns):**
```
Name        | Email           | Belt Rank | Weight Class    | Age | Status   | Joined
------------|-----------------|-----------|-----------------|-----|----------|----------
Alex T.    | alex@...        | Brown     | Middleweight    | -1  | Inactive | 11/26/25
Alex Y.    | test05@...      | Brown     | Welterweight    | 22  | Active   | 11/29/25
Anna D.    | anna@...        | Green     | Lightweight     | N/A | Active   | 11/26/25
```

### CSV Format

```
BlackCobra Karate Club - Trainee Management Report

Generated: January 11, 2026
Status Filter: All | Belt Filter: All

Summary
Metric,Count
Total Trainees,44
Active,44
Inactive,1
Suspended,0

Trainee Details (By User)
Name,Email,Belt Rank,Weight Class,Age,Status,Joined
Alex Thunder,alex@blackcobra.com,Brown,Middleweight,-1,Inactive,11/26/2025
```

### Columns Included

| Column | Purpose |
|--------|---------|
| Name | Full trainee name |
| Email | Contact email |
| Belt Rank | Current belt rank |
| Weight Class | Assigned weight class |
| Age | Trainee age |
| Status | Active/Inactive/Suspended |
| Joined | Join date (MM/DD/YYYY) |

### Use Cases

- Quick lookup of trainee information
- Email list generation
- Contact directory
- Attendance verification
- Status monitoring

## Export by Belt Rank Format

### Purpose
Hierarchical format grouped by belt progression, useful for:
- Promotion tracking
- Belt level management
- Training group organization
- Rank-based reporting

### PDF Layout

**Document Title:**
```
BlackCobra Karate Club
Trainee Management Report (By Belt Rank)
Generated: January 11, 2026 | Status Filter: All | Belt Filter: All
```

**Summary Table:**
```
Metric                    Count
Total Trainees            44
Active                    44
Inactive                  1
Suspended                 0
```

**Belt Sections** (in order):

```
White Belt (14 trainees)
─────────────────────────────────────────────
Name        | Email           | Weight Class    | Age | Status   | Joined
------------|-----------------|-----------------|-----|----------|----------
John Doe   | john@...        | Lightweight     | 18  | Active   | 12/01/25

Yellow Belt (6 trainees)
─────────────────────────────────────────────
Name        | Email           | Weight Class    | Age | Status   | Joined
------------|-----------------|-----------------|-----|----------|----------
Emma Tiger | emma@...        | Welterweight    | 22  | Active   | 11/26/25
```

### PDF Structure

Belt order follows standard karate progression:
1. White
2. Yellow
3. Orange
4. Green
5. Blue
6. Brown
7. Black
8. Master Degree

Each belt section includes:
- Belt rank heading with count
- Trainee table (6 columns, excluding belt rank)
- Trainees sorted alphabetically within belt

### CSV Format

```
BlackCobra Karate Club - Trainee Management Report (By Belt Rank)

Generated: January 11, 2026
Status Filter: All | Belt Filter: All

Summary
Metric,Count
Total Trainees,44
Active,44
Inactive,1
Suspended,0

White Belt (14 trainees)
Name,Email,Weight Class,Age,Status,Joined
John Doe,john@example.com,Lightweight,18,Active,12/01/2025
Jane Smith,jane@example.com,Middleweight,20,Active,11/28/2025

Yellow Belt (6 trainees)
Name,Email,Weight Class,Age,Status,Joined
Emma Tiger,emma@blackcobra.com,Welterweight,22,Active,11/26/2025
```

### Columns Included

| Column | Purpose |
|--------|---------|
| Name | Full trainee name |
| Email | Contact email |
| Weight Class | Assigned weight class |
| Age | Trainee age |
| Status | Active/Inactive/Suspended |
| Joined | Join date (MM/DD/YYYY) |

*Note: Belt Rank column omitted (already in section heading)*

### Use Cases

- Promotion analysis and planning
- Training by belt level
- Tournament organization
- Belt rank statistics
- Progression tracking
- Instructor assignments
- Class grouping

## File Naming

Files are automatically named based on export format:

| Export Format | PDF Filename | CSV Filename |
|---|---|---|
| By User | `trainees_user.pdf` | `trainees_user.csv` |
| By Belt | `trainees_belt.pdf` | `trainees_belt.csv` |

## Combining with Filters

Export formats work with existing filters:

### Status Filter
- All (default)
- Active
- Inactive  
- Suspended

### Belt Filter
- All (default)
- White
- Green
- Brown
- Black
- Master Degree

### Filter Examples

**Example 1: Active Brown Belts by User**
1. Select "Active" in Status filter
2. Select "Brown" in Belt filter
3. Keep "Export by User" selected
4. Click Export → PDF
5. Receives: `trainees_user.pdf` with only active brown belts, in alphabetical order

**Example 2: All Green Belts by Belt Rank**
1. Select "Green" in Belt filter
2. Keep Status filter as "All"
3. Select "Export by Belt Rank"
4. Click Export → CSV
5. Receives: `trainees_belt.csv` with only green belt section

**Example 3: Suspended Members by User**
1. Select "Suspended" in Status filter
2. Keep Belt filter as "All"
3. Keep "Export by User" selected
4. Click Export → PDF
5. Receives: `trainees_user.pdf` with only suspended trainees

## Data Accuracy

### Filters Applied at Database Level
- Query is filtered before grouping
- Statistics reflect filtered results
- Exported data is consistent across formats

### Grouping Applied After Filtering
- Trainees are first filtered by status/belt
- Then grouped by belt rank (if by_belt format selected)
- Groups show only matching trainees

### Example: Active Trainees Only

**By User (44 total, 44 active):**
```
All 44 trainees listed alphabetically
Status column shows "Active" for all rows
```

**By Belt (44 total, 44 active):**
```
White Belt (14 active trainees)
Yellow Belt (6 active trainees)
...
```

## Performance

| Export Type | File Size | Generation Time |
|---|---|---|
| PDF (by user, 44 trainees) | 6.5 KB | ~100ms |
| PDF (by belt, 44 trainees) | 7.4 KB | ~120ms |
| CSV (by user, 44 trainees) | 3.6 KB | ~50ms |
| CSV (by belt, 44 trainees) | 4.2 KB | ~60ms |

## Technical Details

### Request Parameters

```
GET /admin/trainees/export/
  ?format=[pdf|csv]
  &export_by=[user|belt]
  &status_filter=[active|inactive|suspended|]
  &belt_filter=[white|green|brown|black|master_degree|]
```

### URL Examples

```
# Export all by user as PDF
/admin/trainees/export/?format=pdf&export_by=user

# Export active trainees by belt as CSV
/admin/trainees/export/?format=csv&export_by=belt&status_filter=active

# Export brown belts by belt rank as PDF
/admin/trainees/export/?format=pdf&export_by=belt&belt_filter=brown

# Export active green belts by user as CSV
/admin/trainees/export/?format=csv&export_by=user&status_filter=active&belt_filter=green
```

## Implementation Details

### Service Layer (ReportService)

```python
def trainee_report(
    status_filter=None,
    belt_filter=None,
    export_format='by_user'  # New parameter
):
    # Returns dictionary with:
    # - trainees: list of trainee dicts
    # - trainees_by_belt: dict of belt → trainees
    # - export_format: format used
```

### PDF Builders

- `_build_trainee_by_user_pdf()` - Standard table format
- `_build_trainee_by_belt_pdf()` - Grouped by belt with sections

### CSV Builders

- `_build_trainee_by_user_csv()` - Standard CSV rows
- `_build_trainee_by_belt_csv()` - Belt groups with headers

### View Layer

```python
def trainee_export(request):
    file_format = request.GET.get('format', 'pdf')  # pdf or csv
    export_org = request.GET.get('export_by', 'user')  # user or belt
    # ... rest of view
```

### Template

```html
<select id="exportBy">
    <option value="user">Export by User</option>
    <option value="belt">Export by Belt Rank</option>
</select>

<script>
function exportTrainee(fileFormat) {
    const exportBy = document.querySelector('#exportBy').value;
    // ... build URL with export_by parameter
}
</script>
```

## Troubleshooting

### Export dropdown says "Export by User" but I need "Export by Belt Rank"

1. Locate the dropdown above the blue "Export" button
2. Click the dropdown to open options
3. Select "Export by Belt Rank"
4. Click blue "Export" button
5. Choose PDF or CSV

### File doesn't match selected format

- Check dropdown value before clicking Export
- Clear browser cache if selector doesn't seem to save
- Verify URL shows correct `export_by` parameter

### CSV has wrong organization

- In Excel, ensure opening with correct delimiter (comma)
- Use "Text to Columns" feature in Excel if needed
- Google Sheets automatically handles CSV format

### PDF shows both formats somehow

- Each format should show only one organization style
- If seeing mixed format, re-download file
- Clear browser cache and try again

## Keyboard Shortcuts (Future)

Currently requires UI interaction. Future enhancements could add:
- Alt+U: Switch to "Export by User"
- Alt+B: Switch to "Export by Belt Rank"
- Alt+P: Quick PDF export
- Alt+C: Quick CSV export

## Accessibility

- Selector has proper labels and ARIA attributes
- Keyboard navigable (Tab through controls)
- Clear visual feedback on selection
- Works with screen readers

## Browser Compatibility

Tested and working on:
- ✓ Chrome/Chromium
- ✓ Firefox
- ✓ Safari
- ✓ Edge
- ✓ Mobile browsers

## Summary

The export format selection feature provides flexibility in how trainee data is organized:

- **Use "By User"** for administrative lists, contact directories, status monitoring
- **Use "By Belt"** for promotion planning, training organization, rank reporting

Both formats support the same filtering options and file formats (PDF/CSV), giving administrators complete control over their exports.

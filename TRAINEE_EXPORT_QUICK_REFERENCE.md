# Trainee Export - Quick Reference

## What's New

Export trainee lists as PDF or CSV with optional filters directly from the Trainee Management page.

## Quick Start

1. Go to **Admin > Trainee Management** → `http://127.0.0.1:8000/admin/trainees/`
2. (Optional) Apply filters using **Status** and **Belt** dropdowns
3. Click blue **Export** button
4. Choose **Export as PDF** or **Export as CSV**
5. File downloads automatically

## Export Features

### PDF Format
✓ Professional formatting with BlackCobra branding  
✓ Summary statistics table  
✓ 7-column detailed trainee table (Name, Email, Belt Rank, Weight Class, Age, Status, Joined)  
✓ Generated date and filter metadata  
✓ Authorized signature section  
✓ Print-ready styling  

**File**: `trainees_report.pdf`

### CSV Format
✓ Excel/Google Sheets compatible  
✓ Same data as PDF  
✓ Easy to manipulate in spreadsheet applications  
✓ Machine-readable format  

**File**: `trainees_report.csv`

## Filter Combinations

| Status Filter | Belt Filter | Use Case |
|---|---|---|
| All | All | Complete trainee roster |
| Active | All | Current active members |
| Active | Brown | Brown belt candidates |
| Inactive | All | Inactive member list |
| Suspended | All | Suspended members review |
| Any | Black | Black belt list |
| Any | Green | Green belt progress tracking |

## URL Examples

```
# All trainees (PDF)
/admin/trainees/export/?format=pdf

# Active trainees (CSV)
/admin/trainees/export/?format=csv&status_filter=active

# Brown belts (PDF)
/admin/trainees/export/?format=pdf&belt_filter=brown

# Active black belts (CSV)
/admin/trainees/export/?format=csv&status_filter=active&belt_filter=black
```

## Data Included

**Summary Statistics**
- Total trainees
- Active count
- Inactive count
- Suspended count

**Per Trainee**
- Full name
- Email address
- Belt rank
- Weight class
- Age
- Current status
- Join date

## PDF Table Columns

| Name | Email | Belt Rank | Weight Class | Age | Status | Joined |
|------|-------|-----------|--------------|-----|--------|--------|
| Alex Thunder | alex@... | Brown | Middleweight | -1 | Inactive | 11/26/2025 |
| Alex Yellow1 | test05@... | Brown | Welterweight | 22 | Active | 11/29/2025 |

## Requirements

- Admin user account (required)
- Modern web browser
- PDF reader (for PDF files)
- Spreadsheet application (for CSV files)

## Browser Compatibility

✓ Chrome/Chromium  
✓ Firefox  
✓ Safari  
✓ Edge  
✓ Mobile browsers (iOS/Android)  

## File Sizes

- **PDF** (44 trainees): ~6.5 KB
- **CSV** (44 trainees): ~3.6 KB
- Generation time: <200ms

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Button not showing | Clear browser cache, re-login as admin |
| PDF won't open | Update PDF reader app |
| CSV shows garbled text | Open with "Text to Columns" in Excel |
| Filter not applied | Check URL parameters, retry filters |
| Download fails | Check browser download settings |

## Related Features

- **Trainee Search**: Search by name, belt rank, status
- **Trainee Filters**: Filter by status and belt rank
- **Trainee Add/Edit**: Manage trainee information
- **Trainee Archive**: Archive inactive trainees

## Support

For issues or feature requests:
1. Check TRAINEE_EXPORT_IMPLEMENTATION.md for detailed documentation
2. Review test results in test_trainee_report.pdf/.csv
3. Contact system administrator

## Implementation Details

**Backend**
- Service: `ReportService` in `core/services/reports.py`
- View: `trainee_export()` in `core/views/admin.py`
- Route: `/admin/trainees/export/`

**Frontend**
- Template: `templates/admin/trainees/list.html`
- Dropdown menu with PDF/CSV options
- Preserves filter parameters in export links

**Requirements Met**
- 3.1: Trainee listing
- 3.6: Trainee management
- 7.3: Export functionality

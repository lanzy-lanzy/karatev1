# Event Export - Quick Start Guide

## What's New

✅ **Comprehensive Export System** with dynamic filtering
✅ **Multiple Formats**: PDF, CSV, Excel
✅ **Column Customization**: Choose exactly what to include
✅ **Advanced Filtering**: Status, date range, sorting
✅ **Live Preview**: See data before exporting
✅ **Professional Reports**: Branded PDF with statistics

## One-Minute Quick Start

### 1. Go to Export
- Event Management page → Click **"Export Report"** button

### 2. Select Filters (Optional)
- Status types (Draft, Open, Closed, etc.)
- Date range
- Columns to include
- Additional details

### 3. Choose Format
- **PDF** - Professional reports
- **CSV** - Spreadsheet import
- **Excel** - Excel native

### 4. Click Export
File downloads automatically!

## Filter Options

### Status Filters
- ☑ Draft
- ☑ Open for Registration
- ☑ Registration Closed
- ☑ Ongoing
- ☑ Completed
- ☑ Cancelled

### Columns Available
- Event Name
- Event Date
- Location
- Status
- Participants
- Max Capacity
- Registration Deadline
- Description

### Additional Options
- ☐ Include Participants List
- ☐ Include Matches Info
- ☑ Include Summary Statistics

### Sort By
- Event Date (Newest First) ⭐ Default
- Event Date (Oldest First)
- Event Name (A-Z)
- Participants (High to Low)
- Status

## Export Format Details

### PDF Report
Best for: Professional reports, printing, archiving
- Summary statistics
- Formatted data table
- Participants list (if selected)
- Branded styling
- File: `Events_Report_YYYYMMDD_HHMMSS.pdf`

### CSV File
Best for: Spreadsheet import, data analysis
- Clean comma-separated values
- No formatting
- All columns included
- File: `Events_Report_YYYYMMDD_HHMMSS.csv`

### Excel File
Best for: Excel users, advanced analysis
- Currently CSV format (upgradeable)
- Can import to Excel
- File: `Events_Report_YYYYMMDD_HHMMSS.csv`

## Common Use Cases

### 1. Monthly Report
- Status: All checked
- Date: Last 30 days
- Format: PDF
- Columns: Name, Date, Location, Status
- Statistics: Yes

### 2. Participant List
- Columns: Name, Participants, Max Capacity
- Include: Participants List
- Format: PDF
- Sort: By participants (high to low)

### 3. Spreadsheet Analysis
- Format: CSV
- Columns: All
- Status: Open events only
- Sort: By date

### 4. Archive Report
- Status: All except Draft
- Date: All time
- Include: Statistics
- Format: PDF

## Tips & Tricks

💡 **Use Date Range** to limit large datasets
💡 **Select Columns** to reduce file size
💡 **Include Statistics** for context
💡 **Preview** shows exactly what you'll get
💡 **Timestamps** in filenames prevent overwrites

## Accessing Export

**URL**: `/admin/events/export/`

**Button Location**: Event Management → Green "Export Report" button

**Who Can Access**: Admin users only

## Files Included

### System Files
- Core logic: `core/views/admin.py`
- Template: `templates/admin/events/export.html`
- Routes: `core/urls.py`

### Documentation
- Full Guide: `COMPREHENSIVE_EVENT_EXPORT_GUIDE.md`
- This File: `EVENT_EXPORT_QUICK_START.md`

## What Gets Exported

### Summary Statistics
- Total events count
- Open events count
- Completed events count
- Cancelled events count
- Total registered participants

### Event Details
(Depends on column selection)
- Event name
- Event date
- Location
- Status
- Current participants
- Maximum capacity
- Registration deadline
- Description

### Optional Details
- Full participant list with belt rank
- Match information
- Detailed statistics

## File Information

| Aspect | Details |
|--------|---------|
| Formats | PDF, CSV, Excel |
| File Size | 50KB - 200KB (PDF) |
| Generation Time | <2 seconds |
| Download | Automatic |
| Filename Pattern | `Events_Report_YYYYMMDD_HHMMSS.format` |

## System Requirements

✅ Django 5.2+
✅ Python 3.12+
✅ reportlab (already installed)
✅ No additional dependencies

## Troubleshooting

### PDF doesn't download?
- Check browser pop-up settings
- Clear browser cache
- Try different browser

### Filters not working?
- Ensure checkboxes are checked
- Verify form is submitted
- Check admin permissions

### File seems incomplete?
- Preview shows what will be included
- Verify columns are selected
- Check date range

### Need help?
- See `COMPREHENSIVE_EVENT_EXPORT_GUIDE.md`
- Check inline code comments
- Review template structure

## Updates & Changes

**Version 1.0** - Initial release
- Dynamic filtering
- Multiple formats
- Column customization
- Live preview
- Professional PDF styling

## Next Features (Coming Soon)

🔮 True Excel (.xlsx) format
🔮 Email export option
🔮 Scheduled reports
🔮 PDF charts and graphs
🔮 Advanced analytics

---

**Status**: ✅ Ready to Use
**Last Updated**: January 11, 2026
**Support**: See COMPREHENSIVE_EVENT_EXPORT_GUIDE.md for details

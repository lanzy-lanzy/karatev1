# Logo Setup for PDF Exports - Quick Guide

## One-Minute Setup

### Step 1: Prepare Your Logo
- Get your organization logo (PNG format preferred)
- Recommended: 500x500px or larger
- Should have transparent background (optional but better)

### Step 2: Create Media Folder
```bash
mkdir -p karate/media
```

### Step 3: Add Logo
Copy your logo to: `karate/media/logo.png`

### Step 4: Test
1. Go to Event Management
2. Click "Export Report"
3. Export as PDF
4. Logo should appear in header

## That's It! ✅

The system will automatically:
- ✅ Find the logo
- ✅ Add it to every PDF
- ✅ Add "Prepared by" information
- ✅ Add generation timestamp

## Logo Specifications

| Aspect | Recommendation |
|--------|---|
| Format | PNG (JPG works too) |
| Size | 500x500px minimum |
| Color | Any (transparent BG ideal) |
| Location | `karate/media/logo.png` |
| Name | Must be exactly `logo.png` |

## File Structure

```
karate/
├── core/
├── karate/
├── media/               ← Create this folder
│   └── logo.png        ← Put your logo here
├── templates/
└── manage.py
```

## What Appears in PDF

### Header Section:
```
[Logo Icon] BlackCobra Karate Club
            Event Management Report

Report Information
Generated on: January 11, 2026 at 5:45 PM
Prepared by: John Smith (Admin)
Total Events: 15
```

### What's Automatic:
- ✅ Logo appears (if file exists)
- ✅ Organization name shown
- ✅ Current date/time added
- ✅ Admin username added
- ✅ Event count calculated

## Getting a Logo

### Option 1: Use Existing Logo
If your organization has a logo file:
1. Get the PNG/JPG file
2. Resize to 500x500px if needed
3. Save as `logo.png`
4. Place in `karate/media/`

### Option 2: Create Simple Logo
Tools to create a simple logo:
- Canva (canva.com) - Free online
- Photopea (photopea.com) - Free online
- GIMP - Free desktop app
- Inkscape - Free vector editor

### Option 3: Use Placeholder
Download a placeholder:
1. Visit icons.org or pngimg.com
2. Search "karate logo" or "martial arts"
3. Download PNG
4. Save as `logo.png`

## Troubleshooting

### Logo not showing?
**Check 1**: File exists?
```bash
ls -la karate/media/logo.png
```

**Check 2**: File is readable?
```bash
file karate/media/logo.png
```

**Check 3**: Right location?
Path must be: `karate/media/logo.png`

### Still not working?
The export will still work without logo - it just uses text header instead.

## Verify Setup

### Test Export
1. Go to `/admin/events/`
2. Click "Export Report"
3. Select PDF format
4. Click "Export Report"
5. Check PDF header for logo

### Check CSV
1. Export as CSV
2. Open in text editor
3. First line should be: "BlackCobra Karate Club - Event Report"
4. Second line: "Generated on: ..."
5. Third line: "Prepared by: ..."

## Optional: Customize Logo Size

If logo appears too small or too large, edit:

**File**: `core/views/admin.py`

**Find**: Line with `Image(logo_path, width=0.5*inch, height=0.5*inch)`

**Change**:
```python
# Larger logo
logo = Image(logo_path, width=0.75*inch, height=0.75*inch)

# Smaller logo
logo = Image(logo_path, width=0.35*inch, height=0.35*inch)
```

Then test again.

## What's Included in Exports

### PDF Header (Automatic)
- Organization logo (if file exists)
- Organization name
- Report title
- Generation date/time
- Prepared by (current admin user)
- Total events count

### CSV Header (Automatic)
- Organization name
- Generation date/time
- Prepared by (current admin user)
- Empty line for spacing

## Security Note

✅ No sensitive information exposed
✅ Only admin can access exports
✅ User information is just name/username
✅ No passwords or keys leaked

## Files Modified

Only backend code updated:
- ✅ `core/views/admin.py` - Export functions

No frontend changes needed.

## Support

If logo doesn't appear:
1. Verify file exists at `karate/media/logo.png`
2. Check file format (PNG or JPG)
3. Ensure file is readable
4. Export still works without logo (uses text)

## Next Steps

1. ✅ Prepare your logo file
2. ✅ Create `media/` folder
3. ✅ Copy logo as `logo.png`
4. ✅ Test export
5. ✅ Done!

---

**Time to Setup**: 2 minutes
**Complexity**: Minimal (just copy file)
**Result**: Professional branded PDF exports

Your exports are now ready to be branded with your organization logo! 🎯

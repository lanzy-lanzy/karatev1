# PDF Report Header Layout Update

## Changes Made

Updated all PDF report exports (membership, financial, and event reports) with a new professional header layout:

### Header Layout
```
[Logo]     [Organization Name - Centered]     [Judo Logo]
(Left)     BLACK COBRA JUDO                     (Right)
           KARATE AIKIDO
           ASSOCIATION OF THE
           PHILIPPINES
```

### Features

1. **Left Logo**: Black Cobra logo (1" x 1")
   - File: `core/static/images/black_cobra_logo.jpg`
   - Already exists

2. **Center Text**: Organization name (Bold, 13pt, Centered)
   - "BLACK COBRA JUDO KARATE AIKIDO ASSOCIATION OF THE PHILIPPINES"
   - Split across 4 lines for better readability
   - Line height: 16pt

3. **Right Logo**: Judo/Martial Arts logo (1" x 1")
   - File: `core/static/images/judo_logo.png`
   - **TODO: This file needs to be added**

### Layout Details

- **Page Width**: 8.5" (letter size)
- **Left Column**: 1.2" (logo)
- **Center Column**: 3.6" (text)
- **Right Column**: 1.2" (logo)
- **Vertical Alignment**: Middle (centered)
- **Padding**: Minimal to maximize space

### Files Modified

- `core/services/reports.py`
  - `_build_membership_pdf()` - Updated header
  - `_build_financial_pdf()` - Updated header
  - `_build_event_pdf()` - Updated header

### Next Steps

1. **Add Judo Logo**: Add a judo/martial arts logo image to:
   - Path: `core/static/images/judo_logo.png`
   - Recommended format: PNG with transparency
   - Recommended size: 200x200px (will be scaled to 1"x1")

2. **Test PDF Generation**: Run the test script
   ```bash
   python test_pdf_generation.py
   ```

3. **Verify Output**: Check that:
   - Logos are properly positioned (left and right)
   - Organization text is centered
   - Layout is balanced and professional

### Fallback Behavior

If the judo logo file is missing:
- PDF will still generate successfully
- Right side will show "Judo\nLogo" placeholder text
- Once the logo file is added, it will automatically display in all reports

### Testing

To test the PDF generation locally:
```bash
python test_pdf_generation.py
```

This will create a `test_report.pdf` file showing the new layout.

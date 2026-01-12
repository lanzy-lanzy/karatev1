# Last Edited Feature - Code Reference

## Quick Code Lookup

### Model Definition
**File**: `core/models.py` (line 75)
```python
class Trainee(models.Model):
    # ... other fields ...
    joined_date = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # ← NEW FIELD
```

### Template Display - Desktop
**File**: `templates/admin/trainees/list_partial.html`

**Table Header** (line 61):
```django
<th scope="col" class="px-6 py-4 text-left text-xs font-semibold text-gray-300 uppercase tracking-wider">Last Edited</th>
```

**Table Cell** (lines 118-125):
```django
<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-400">
    <span title="{{ trainee.updated_at|date:'Y-m-d H:i:s' }}">
        {% load humanize %}
        {{ trainee.updated_at|timesince }} ago
    </span>
</td>
```

### Template Display - Mobile
**File**: `templates/admin/trainees/list_partial.html`

**Card Field** (lines 222-229):
```django
<div>
    <p class="text-xs text-gray-400 mb-1">Last Edited</p>
    <p class="font-semibold text-white" title="{{ trainee.updated_at|date:'Y-m-d H:i:s' }}">
        {% load humanize %}
        {{ trainee.updated_at|timesince }} ago
    </p>
</div>
```

### Migration File
**File**: `core/migrations/0026_trainee_updated_at.py`
```python
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0025_alter_beltrankprogress_new_belt_rank_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainee',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
```

### Django Settings
**File**: `karate/settings.py` (line 40)
```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",  # ← ADDED
]
```

---

## Template Variables Reference

### Available in Template Context
```django
{{ trainee.updated_at }}              # Raw datetime object
{{ trainee.updated_at|date:'Y-m-d' }} # Formatted: 2026-01-11
{{ trainee.updated_at|time:'H:i:s' }} # Formatted: 14:30:45
{{ trainee.updated_at|timesince }}    # Relative: "5 minutes"
{{ trainee.updated_at|timesince }} ago # Output: "5 minutes ago"
```

### CSS Classes Used
```css
px-6 py-4              /* Padding */
whitespace-nowrap      /* Prevent wrapping */
text-sm                /* Font size */
text-gray-400          /* Light gray color */
title                  /* Tooltip attribute (HTML) */
```

---

## Data Flow Diagram

```
User Action
    ↓
[Click Edit Button]
    ↓
[Modify Trainee Form]
    ↓
[Submit POST Request]
    ↓
trainee_edit() View
    ↓
trainee.save()  ← auto_now updates updated_at
    ↓
Database Commit
    ↓
Redirect to List
    ↓
Template Renders
    ↓
{{ trainee.updated_at|timesince }} ago
    ↓
Display: "1 minute ago"
```

---

## Template Inheritance Chain

```
admin/trainees/list.html
    ↓
{% include 'admin/trainees/list_partial.html' %}
    ↓
For each trainee:
    ├─ Desktop: Render table row with all columns
    │   └─ Last Edited cell: {{ trainee.updated_at|timesince }} ago
    │
    └─ Mobile: Render card view
        └─ Last Edited field in grid
```

---

## Database Schema Change

### Before
```sql
CREATE TABLE core_trainee (
    id INTEGER PRIMARY KEY,
    profile_id INTEGER UNIQUE NOT NULL,
    belt_rank VARCHAR(20) NOT NULL,
    weight DECIMAL(5,2) NOT NULL,
    weight_class VARCHAR(20),
    emergency_contact VARCHAR(100) NOT NULL,
    emergency_phone VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL,
    archived BOOLEAN NOT NULL,
    joined_date DATE NOT NULL,
    FOREIGN KEY(profile_id) REFERENCES core_userprofile(id)
);
```

### After
```sql
CREATE TABLE core_trainee (
    id INTEGER PRIMARY KEY,
    profile_id INTEGER UNIQUE NOT NULL,
    belt_rank VARCHAR(20) NOT NULL,
    weight DECIMAL(5,2) NOT NULL,
    weight_class VARCHAR(20),
    emergency_contact VARCHAR(100) NOT NULL,
    emergency_phone VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL,
    archived BOOLEAN NOT NULL,
    joined_date DATE NOT NULL,
    updated_at DATETIME NOT NULL,  -- ← NEW COLUMN
    FOREIGN KEY(profile_id) REFERENCES core_userprofile(id)
);
```

---

## Filter & Tag Reference

### Django Humanize Filters
```django
{% load humanize %}

{{ datetime_value|timesince }}
  Returns: "5 minutes" (no "ago")
  
{{ datetime_value|timesince:reference_date }}
  Returns: Time difference from reference date

{{ datetime_value|timeuntil }}
  Returns: Time until future date
```

### Django Date Filters
```django
{{ datetime_value|date:"Y-m-d" }}      # 2026-01-11
{{ datetime_value|date:"Y-m-d H:i:s" }} # 2026-01-11 14:30:45
{{ datetime_value|time:"H:i:s" }}      # 14:30:45
{{ datetime_value|date:"F j, Y" }}     # January 11, 2026
```

---

## Testing Code Snippets

### Check Field Exists
```python
from core.models import Trainee
t = Trainee.objects.first()
print(t.updated_at)  # Should print datetime
```

### Check Migration Applied
```bash
python manage.py showmigrations core | grep 0026
# Should show: [X] 0026_trainee_updated_at
```

### Check Humanize Loaded
```bash
python manage.py shell
>>> from django.template import defaultfilters
>>> from datetime import timedelta
>>> from django.utils import timezone
>>> now = timezone.now()
>>> past = now - timedelta(minutes=5)
>>> defaultfilters.timesince(past)
'5 minutes'
```

---

## Common Django Commands

```bash
# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations core

# Reverse migration (if needed)
python manage.py migrate core 0025_alter_beltrankprogress_new_belt_rank_and_more

# Create backup before changes
python manage.py dumpdata core.Trainee > trainee_backup.json

# Load data from backup
python manage.py loaddata trainee_backup.json

# Django shell for testing
python manage.py shell
```

---

## Browser DevTools Tips

### Check Rendered HTML
```html
<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-400">
    <span title="2026-01-11 14:30:45">
        5 minutes ago
    </span>
</td>
```

### Check Hover Tooltip
- Right-click element
- Select "Inspect Element"
- See `title` attribute value
- Shows exact datetime

### Network Tab
- Check POST request to edit endpoint
- Response should redirect to list
- New trainee list rendered with updated timestamp

---

## Backward Compatibility

✅ **Fully Compatible**
- No breaking changes to API
- Existing code not affected
- Optional field for reading (not required for writes)
- Migration is reversible if needed
- Database change is additive (no deletions)

---

## File Locations Quick Reference

```
karate/
├── karate/
│   └── settings.py                    ← Humanize app config
├── core/
│   ├── models.py                      ← Trainee.updated_at field
│   └── migrations/
│       └── 0026_trainee_updated_at.py ← Database migration
└── templates/
    └── admin/
        └── trainees/
            ├── list_partial.html      ← Active trainees view
            └── archived_partial.html  ← Archived trainees view
```

---

## Summary Statistics

- **Lines Added**: ~40 (templates)
- **Database Columns Added**: 1
- **New Files**: 1 (migration)
- **Files Modified**: 4
- **Django Apps Added**: 1 (humanize)
- **Performance Impact**: Negligible
- **Breaking Changes**: None

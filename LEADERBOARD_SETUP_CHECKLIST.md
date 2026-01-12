# Leaderboard Admin Setup Checklist

## Files Modified/Created

### 1. View Function Added ✅
- **File**: `core/views/admin.py`
- **Line**: 2724
- **Function**: `leaderboard_view(request)`
- **Status**: Defined with @admin_required decorator

### 2. URL Route Added ✅
- **File**: `core/urls.py`
- **Line**: 102
- **Route**: `path('admin/leaderboard/', admin_views.leaderboard_view, name='admin_leaderboard')`
- **Status**: Registered

### 3. Sidebar Link Added ✅
- **File**: `templates/components/sidebar_admin.html`
- **Lines**: 463-469
- **Status**: Added to admin navigation section

### 4. Template Created ✅
- **File**: `templates/admin/leaderboard/list.html`
- **Status**: Full template with styling

### 5. Sidebar Made Scrollable ✅
- **File**: `templates/components/sidebar.html`
- **Lines**: 72-93
- **Status**: Added overflow-y: auto and scrollbar styling

## What You Need to Do

1. **Restart Django Server**
   ```bash
   # Stop the current server (Ctrl+C)
   # Then restart it
   python manage.py runserver
   ```

2. **Clear Browser Cache**
   - Hard refresh: `Ctrl+Shift+R` (Windows/Linux)
   - Or: `Cmd+Shift+R` (Mac)

3. **Verify Installation**
   - Navigate to `/admin/leaderboard/` directly in the browser
   - Should see the leaderboard page
   - Sidebar should show "Leaderboard" link at the bottom

## Expected Result

After restarting Django and clearing browser cache:
- Sidebar will have "Leaderboard" link after "Evaluations"
- Sidebar will be scrollable if content exceeds viewport
- Link will navigate to `/admin/leaderboard/` page
- Page will display leaderboard rankings with timeframe filters

## Troubleshooting

If still not visible:
1. Check Django console for any import errors
2. Verify you're logged in as admin user
3. Check that URL name `admin_leaderboard` is accessible in Django shell:
   ```bash
   python manage.py shell
   >>> from django.urls import reverse
   >>> reverse('admin_leaderboard')
   '/admin/leaderboard/'
   ```
4. Check browser developer console for any template errors

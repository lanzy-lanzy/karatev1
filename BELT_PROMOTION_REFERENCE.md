# Belt Promotion Feature - Quick Reference

## Access Point
**Sidebar → Admin Dashboard → Belt Promotion**

## Main Operations

### Promote a Trainee
1. Belt Promotion → Find trainee → Click "Promote"
2. Select new belt rank
3. (Optional) Add admin notes
4. Click "Promote Trainee"
5. ✓ Trainee notified automatically

### Search Trainee
- Type in search box (live search)
- Filter by belt rank
- Filter by status (active/inactive/suspended)

### View Promotion History
- Click "Promotion History" button
- See all promotions with details
- Filter by trainee

## Database Tables Updated

### BeltRankProgress (Enhanced)
- `promotion_type`: 'automatic' or 'admin_override'
- `admin_notes`: Text field for documentation
- `promoted_by`: Foreign key to User (who made change)

## New Views (Backend)

```python
# Location: core/views/admin.py

belt_rank_promotion_list()          # Main list page
belt_rank_promotion_list_partial()  # HTMX partial
belt_rank_promote()                 # Promotion form + handler
belt_rank_promotion_history()       # History page
```

## New URLs

| URL | Method | Purpose |
|-----|--------|---------|
| `/admin/belt-promotion/` | GET | Main list |
| `/admin/belt-promotion/partial/` | GET | HTMX updates |
| `/admin/belt-promotion/<id>/promote/` | GET/POST | Promote form |
| `/admin/belt-promotion/history/` | GET | History view |

## New Templates

```
templates/admin/belt_promotion/
├── list.html           # Main page
├── list_partial.html   # Table rows (HTMX)
├── promote_form.html   # Promotion form
├── history.html        # History page
└── history_partial.html # History cards
```

## Key Features

| Feature | Details |
|---------|---------|
| Override Rank | Promote to any valid belt |
| Audit Trail | Track who, when, and why |
| Notifications | Auto-notify trainee |
| Search | Real-time by name |
| Filter | By belt or status |
| History | Complete promotion log |
| Mobile | Fully responsive |

## Validation Rules

✓ Can promote to different rank
✗ Cannot promote to same rank
✓ Can only use valid belt ranks
✓ Validates on server-side

## Notification Details

When trainee is promoted:
- **Type**: belt_promotion
- **Title**: "Belt Promotion to [Belt Name]"
- **Message**: "Congratulations! Your belt rank has been promoted..."
- **Recipient**: The promoted trainee
- **Delivery**: In-app notification

## Admin Notes Examples

```
"Promoted due to tournament victory"
"Makeup for system downtime"
"Re-tested and passed criteria"
"Recognition for leadership"
"Benchmark achievement reached"
```

## Color-Coded Belt Ranks

| Belt | Color |
|------|-------|
| White | Gray (#FFF) |
| Yellow | Gold (#FFC107) |
| Orange | Orange (#FF9800) |
| Green | Green (#4CAF50) |
| Blue | Blue (#2196F3) |
| Brown | Brown (#795548) |
| Black | Black (#000) |

## Promotion Type Badges

- 🟠 **Admin Override**: Manual promotion by admin
- 🟢 **Automatic**: System auto-promotion via points

## Information Displayed

### On List Page
- Trainee name & email
- Current belt rank
- Total points
- Status
- Promote button

### On Promotion Form
- Avatar/initials
- Current belt rank
- Points earned
- Status
- Weight class
- Promotion history (if exists)
- New belt selector
- Admin notes field

### In History
- Trainee info
- Belt transition (old → new)
- Promotion type
- Date & time
- Points at promotion
- Admin who promoted
- Admin notes (if any)

## Keyboard Shortcuts

None implemented (standard form submission)

## Browser Compatibility

✓ Chrome, Firefox, Safari, Edge
✓ Mobile browsers
✓ Tablet browsers
✓ Requires JavaScript enabled (HTMX)

## Performance Tips

1. Search typing is debounced (300ms)
2. Filters use HTMX (no full page reload)
3. Queries optimized with select_related()
4. Mobile-friendly with responsive design

## Security Notes

- 🔐 Admin-only access required
- 🔐 User authentication required
- 🔐 CSRF protection on forms
- 🔐 Server-side validation
- 🔐 SQL injection protection (Django ORM)

## Database Migration

Ran successfully:
```
core/migrations/0008_beltrankprogress_admin_notes_and_more.py
- Added promotion_type field
- Added admin_notes field
- Added promoted_by field
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Belt Promotion not in sidebar | Check admin login |
| Can't select belt | Make sure it's different from current |
| Trainee not notified | Check Notification records |
| Search not working | Wait 300ms (debounce) |
| Page not loading | Check browser console |

## Related Features

- **Leaderboard**: Shows belt-rank based rankings
- **Notifications**: Handles trainee notifications
- **Trainee Profile**: Shows current belt rank
- **Reports**: Can include belt rank statistics

## Statistics to Track

- Total promotions (automatic vs override)
- Most promoted belt rank
- Admin with most promotions
- Average time between promotions
- Trainees promoted today/week/month

## API/Access

All features accessible via:
- Web UI (admin dashboard)
- URL routes (Django)
- Database (direct ORM access)

No REST API implemented (future enhancement)

## Admin Permissions Required

- Role: `admin`
- Access: `@admin_required` decorator
- No additional permissions needed

## Related Settings

No additional Django settings required.
Uses default Django permissions system.

## Logs to Check

- Django logs: Promotion attempts
- Database logs: Changes to BeltRankProgress
- Server logs: Admin actions

## Backup Considerations

- Promotions are permanent (no delete)
- History cannot be edited
- Admin notes are immutable
- Promotion_type cannot be changed

System is append-only for audit trail integrity.

---

**Last Updated**: 2024-11-27
**Status**: ✓ Production Ready
**Tested**: ✓ Full system test passed

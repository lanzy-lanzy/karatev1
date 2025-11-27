# Belt Promotion Quick Start Guide

## What Was Added

### New Files
1. **Templates** (4 new files in `templates/admin/belt_promotion/`)
   - `list.html` - Main promotion management page
   - `list_partial.html` - HTMX partial for filtering
   - `promote_form.html` - Promotion form with trainee details
   - `history.html` & `history_partial.html` - Promotion history

2. **Backend**
   - 4 new views in `core/views/admin.py`
   - Updated models in `core/models.py`
   - 4 new URL routes in `core/urls.py`
   - Updated sidebar navigation in `templates/components/sidebar_admin.html`

3. **Database**
   - Migration file: `core/migrations/0008_...py`

### What It Does

**Belt Promotion Management** allows admins to:
- View all trainees with current belt ranks
- Search and filter trainees
- Override a trainee's belt rank to any valid rank
- Add admin notes explaining the reason
- Track all promotions (automatic and manual)
- Send automatic notifications to promoted trainees

## Quick Steps to Use

### Step 1: Login as Admin
Navigate to your karate admin dashboard

### Step 2: Access Belt Promotion
Click **"Belt Promotion"** in the left sidebar

### Step 3: Find a Trainee
- Scroll through the list, OR
- Search by name in the search box, OR
- Filter by belt rank or status

### Step 4: Click Promote
Click the blue "Promote" button on any trainee row

### Step 5: Select New Rank
- Choose the new belt rank from the dropdown
- (Optional) Add admin notes explaining why
- Click "Promote Trainee"

Done! The trainee is promoted and notified.

## Key Features

### Search & Filter
- **Search**: Real-time search by name or username
- **Belt Filter**: Show only trainees of specific belt
- **Status Filter**: Show only active/inactive/suspended trainees

### Information Shown
- Trainee name and email
- Current belt rank (with color coding)
- Total points earned
- Current status
- Promotion history (on detail page)

### Color-Coded Belts
- White: Gray
- Yellow: Gold
- Orange: Orange
- Green: Green
- Blue: Blue
- Brown: Brown
- Black: Black

### Admin Notes
When promoting, you can add notes like:
- "Promoted due to tournament performance"
- "Makeup for system downtime"
- "Special recognition award"
- "Re-tested and passed assessment"

These notes are stored in the promotion history for audit trail.

## Promotion History

Click **"Promotion History"** to see:
- All past promotions (automatic and admin overrides)
- Who made the change (for overrides)
- When it happened
- Why (admin notes)
- Points at time of promotion

## Important Notes

✓ **What You Can Do:**
- Promote to any belt rank (not just next rank)
- Add notes for documentation
- View complete history
- Search and filter trainees
- See points and status

✗ **What You Can't Do:**
- Promote to same rank (validation prevents this)
- Promote to invalid belt (system validates)
- See promotions without admin access

## URL Reference

| Page | URL |
|------|-----|
| Main List | `/admin/belt-promotion/` |
| Promote Trainee | `/admin/belt-promotion/<trainee_id>/promote/` |
| History | `/admin/belt-promotion/history/` |

## Notifications

When you promote a trainee:
1. Their belt rank is immediately updated
2. They receive an in-app notification
3. The change is logged in promotion history
4. The notification shows which belt they were promoted to

## Database Impact

The system:
- ✓ Creates promotion records automatically
- ✓ Updates trainee belt rank
- ✓ Tracks who made the change
- ✓ Preserves all history
- ✓ No data is deleted

## Mobile Friendly

The interface works on:
- Desktop browsers
- Tablets
- Mobile phones

All filtering and actions work seamlessly on mobile.

## Troubleshooting

**Can't find "Belt Promotion" in sidebar?**
- Make sure you're logged in as an admin
- Check that sidebar is fully loaded

**Can't promote a trainee?**
- Make sure you selected a different belt rank
- Verify the new rank is valid (not same as current)
- Check browser console for errors

**Don't see promotion history?**
- Promotions only appear after they're created
- Check that trainee has had promotions

**Search not working?**
- Wait a moment (300ms debounce on search)
- Try searching by first or last name
- Clear filters and try again

## Support

For technical issues, check:
1. Django admin logs
2. Browser console (F12)
3. Server error logs
4. Database records in `core_beltrankprogress` table

## Next Steps

You can:
1. Promote trainees based on tournament performance
2. Create makeup promotions for system downtime
3. Review promotion history for audit purposes
4. Track which admin made which changes
5. Communicate changes to trainees via notifications

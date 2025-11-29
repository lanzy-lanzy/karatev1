# Judge Management System - Admin Guide

## Overview
The Judge Management system allows admins to create, edit, and manage judges directly through the admin dashboard sidebar. No need to manually create users anymore - everything is integrated into the admin interface.

## Features

✅ **Create New Judges** - Register judges with certification information  
✅ **Edit Judge Details** - Update judge information and certification  
✅ **Deactivate/Archive Judges** - Temporarily disable judges from being assigned  
✅ **Restore Archived Judges** - Reactivate deactivated judges  
✅ **Search & Filter** - Find judges by name, email, certification level  
✅ **Active & Archived Lists** - Separate views for active and inactive judges  

## Accessing Judge Management

### From the Admin Sidebar
1. Log in as Admin
2. Look for "Judge Management" in the left sidebar (below "User Management")
3. Click to view all active judges

### Direct URL
- Active Judges: `/admin/judges/`
- Archived Judges: `/admin/judges/archived/`

## Creating a New Judge

### Step-by-Step

**1. Click "Judge Management" in Sidebar**
   - You'll see the judges list page

**2. Click "Add Judge" Button (top-right)**
   - You'll be taken to the judge creation form

**3. Fill in Personal Information**
   - **First Name** (required) - Judge's first name
   - **Last Name** (required) - Judge's last name
   - **Email** (required) - Unique email address
   - **Phone** (optional) - Contact phone number

**4. Fill in Account Information**
   - **Username** (required) - Login username for the judge
   - Must be unique in the system
   - Example: `judge_sarah`, `judge_ahmed`

**5. Fill in Certification Information**
   - **Certification Level** (required) - Select from:
     - Regional (lowest level)
     - National (intermediate level)
     - International (highest level)
   - **Certification Date** (required) - When they were certified

**6. Click "Create Judge"**
   - Judge account is created automatically
   - Judge is assigned the "Judge" role
   - Judge is set as active by default
   - Success message is shown

### What Gets Created
When you create a judge, the system automatically creates:
- A User account (for login)
- A UserProfile (role = "judge")
- A Judge record (with certification info)

The judge can then log in with:
- Username: [username you entered]
- Password: [they'll set on first login or you can provide]

## Editing a Judge

**1. From Judge List**
   - Find the judge in the list
   - Click the "Edit" button

**2. Modify Information**
   - Change first name, last name, phone
   - Update certification level and date
   - Toggle "Judge is active" checkbox
   - **Note:** Email and username cannot be changed

**3. Click "Update Judge"**
   - Changes are saved immediately
   - Success message is shown

## Deactivating/Archiving a Judge

When a judge should no longer be assigned to matches:

**1. From Judge List**
   - Find the judge
   - Click the "Deactivate" button
   - Confirm the action

**2. What Happens**
   - Judge becomes inactive
   - No longer appears in match assignment dropdowns
   - Moves to "Archived Judges" list
   - Can be restored anytime

## Restoring an Archived Judge

To reactivate a deactivated judge:

**1. Go to "Archived Judges"**
   - Click "View Archived Judges" link at bottom of judges list
   - Or go to: `/admin/judges/archived/`

**2. Find the Judge**
   - Use search if needed

**3. Click "Restore" Button**
   - Judge becomes active again
   - Returns to main judges list
   - Can be assigned to matches

## Searching & Filtering Judges

### Search
- Search by: Name, Email, Username
- Real-time filtering as you type
- Clears field to reset

### Filter by Certification Level
- Select level from dropdown:
  - Regional
  - National  
  - International
- Shows only judges with that certification

### Combine Search + Filter
You can use both at the same time:
- Search for "Sarah" AND filter for "National" level
- Shows only national-level judges named Sarah

## Judge Information at a Glance

### Judge List View
Each judge shows:
- **Full Name** with username
- **Email Address**
- **Certification Level** (color-coded badge)
- **Certification Date**
- **Action Buttons** (Edit, Deactivate/Restore)

### Color Coding
- **Purple Badge** = International Certification
- **Blue Badge** = National Certification
- **Gray Badge** = Regional Certification

## Best Practices

### ✅ Do's
- Create judges with clear, memorable usernames
- Use real certification dates and levels
- Regularly update judge information
- Archive judges who are no longer available
- Restore judges if needed later

### ❌ Don'ts
- Don't create duplicate judge records
- Don't use the same email for multiple judges
- Don't use the same username for multiple judges
- Don't leave certification dates in the future
- Don't delete judges (use deactivate instead)

## Common Tasks

### "I need to update a judge's certification"
1. Go to Judge Management
2. Find judge in list
3. Click "Edit"
4. Update certification level and/or date
5. Click "Update Judge"

### "A judge is no longer available, what do I do?"
1. Find judge in list
2. Click "Deactivate"
3. Confirm
4. Judge no longer appears in match assignments
5. Can restore later if needed

### "I deleted a judge by accident, can I get them back?"
1. Check "Archived Judges" list
2. If not there, the judge may have been fully deleted
3. You can create a new judge record if needed

### "I need to assign a judge to matches now"
1. Create the judge first via Judge Management
2. Then go to Matches → Add Match (or Auto-Matchmaking)
3. Judge will appear in the judge selection dropdown
4. Requires minimum 3 judges per match

## Integration with Matches

### When Creating/Editing Matches
- Only **active judges** appear in the judge dropdown
- Deactivated judges are hidden
- You must select **at least 3 judges** per match
- The same judges can be assigned to multiple matches

### When Using Auto-Matchmaking
- Select 3+ judges before creating auto-matched games
- Those judges are assigned to ALL selected matches
- Judges must be active to be selectable

## Database Structure

### User Account
- Django User model for authentication
- Username & email for login
- First/last name for display

### User Profile
- Links User to judge role
- Phone number storage
- Role-based access control

### Judge Record
- Certification level
- Certification date
- Active/inactive status
- Links to matches assigned

## Troubleshooting

### "Email already exists" error
- Email is unique in the system
- Check if judge was already created
- Use different email address

### "Username already exists" error
- Username must be unique
- Try: judge_[name]_[number]
- Examples: judge_sarah_001, judge_ahmed_02

### Judge not appearing in match dropdown
- Judge must be **active** (check archived list)
- Make sure it was created successfully
- Try refresh the page

### Can't edit email or username
- These are locked after creation for security
- If you need to change, create a new judge
- Old one can be archived

## Support

For issues or questions:
1. Check this guide
2. Contact the system administrator
3. Check the system logs for errors

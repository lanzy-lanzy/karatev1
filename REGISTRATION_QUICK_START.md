# Registration System - Quick Start

## What's New

A complete **User Registration & Admin Approval System** has been added to your karate club application. Users can now register, upload required documents, and admins can approve or reject applications.

---

## Quick Access

| Action | URL |
|--------|-----|
| **Register** | `/register/` |
| **Admin Registration List** | `/admin/registrations/` |
| **Login** | `/login/` |

---

## For Users: How to Register

1. **Visit Registration Page**
   - Click "Create one now" on the login page
   - Or go directly to `/register/`

2. **Fill in Personal Information**
   - First & Last Name
   - Email & Phone
   - Date of Birth
   - Current Belt Level (White, Yellow, etc.)

3. **Upload Required Documents**
   - Medical Certificate (PDF/JPG/PNG)
   - Waiver Form (PDF/JPG/PNG)
   - ⚠️ Note: $100 membership fee required (displayed in alert)

4. **Create Account**
   - Set Password
   - Confirm Password
   - Click "Create Account & Submit for Review"

5. **Wait for Admin Approval**
   - Your registration is now **Pending Review**
   - Admin will review your documents
   - You'll be approved or rejected
   - Pay membership fee before admin approves

---

## For Admins: How to Manage Registrations

### View All Registrations
1. Log in as admin
2. Click **"User Management"** in sidebar (top after Dashboard)
3. See list of all registrations with:
   - Status badges (Pending, Approved, Rejected)
   - Payment status (Paid, Unpaid)
   - Quick stats (4 cards at top)

### Search & Filter
- **Search:** Find by name or email
- **Status Filter:** Pending, Approved, or Rejected
- **Payment Filter:** Paid or Unpaid

### Review Individual Registration
1. Click **"View"** button on any registration
2. See:
   - All personal information
   - Download medical certificate
   - Download waiver form
   - Current status & payment info

### Approve Registration
1. On detail page, scroll to "Admin Actions" section
2. *(Optional)* Check "Mark as Payment Paid" if user paid
3. Click **"Approve Registration"** button
4. User can now log in as trainee member

### Reject Registration
1. On detail page, scroll to "Admin Actions" section
2. Enter rejection reason (optional)
3. Click **"Reject Registration"** button
4. User notified of rejection

---

## Quick Stats

On the registrations list, see:
- 📋 **Pending Registrations** - Awaiting review
- ✅ **Approved Members** - Ready to use
- 💳 **Paid Memberships** - Payments received
- ❌ **Rejected Registrations** - Declined applications

---

## Features Included

✅ Beautiful registration form with dark theme  
✅ Document upload (medical cert + waiver)  
✅ $100 membership fee alert (prominent warning)  
✅ Payment tracking (paid/unpaid status)  
✅ Admin approval/rejection  
✅ Search and filtering  
✅ Document download links  
✅ Review tracking (who reviewed & when)  
✅ Rejection reason storage  
✅ Auto user account creation  

---

## Important Notes

### For Users
- ⚠️ Must upload both medical certificate AND waiver
- 💰 $100 membership fee must be paid
- ⏳ Approval process may take 1-2 business days
- 🔒 Password must be at least 8 characters
- 📧 Email is used as backup username

### For Admins
- Only approved users can access trainee dashboard
- Payment status must be tracked
- Documents are downloadable for verification
- Can add rejection reason for records
- Approved users automatically get 'trainee' role

---

## File Locations

```
New Files:
- templates/auth/register.html              ← Registration form
- templates/admin/registrations/list.html   ← Admin list view
- templates/admin/registrations/detail.html ← Admin detail view
- core/views/admin_registrations.py         ← Admin views
- REGISTRATION_SYSTEM_GUIDE.md              ← Full documentation

Updated Files:
- core/models.py                            ← Added Registration model
- core/forms.py                             ← Added RegistrationForm
- core/urls.py                              ← Added registration routes
- templates/auth/login.html                 ← Added register link
- templates/components/sidebar_admin.html   ← Added menu item
```

---

## Database

Migration applied: `0009_registration.py`

Uploaded files stored in:
- `media/registrations/medical_certs/`
- `media/registrations/waivers/`

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Registration page shows 404 | Run migrations: `python manage.py migrate` |
| Can't upload files | Ensure `media/` folder exists with proper permissions |
| User Management link missing | Clear browser cache and refresh |
| Files not downloading | Check media folder path in settings.py |
| Can't approve registration | Ensure you're logged in as admin |

---

## URLs Summary

```python
GET  /register/                                   → Registration form
POST /register/                                   → Submit registration

GET  /admin/registrations/                        → List all registrations
GET  /admin/registrations/<id>/                   → View details
POST /admin/registrations/<id>/                   → Approve/Reject
POST /admin/registrations/<id>/approve/           → Quick approve
POST /admin/registrations/<id>/reject/            → Quick reject
```

---

## Next Steps

1. ✅ **Test Registration:** Visit `/register/` and submit test application
2. ✅ **Admin Review:** Go to `/admin/registrations/` and review applications
3. ✅ **Approve Test User:** Click approve on test registration
4. ✅ **Verify Access:** Test approved user can login and access dashboard
5. 📝 **Customize:** Adjust membership fee in Registration model if needed

---

## Support & Customization

Need to modify something? See **REGISTRATION_SYSTEM_GUIDE.md** for:
- Changing membership fee
- Adding more fields
- Customizing email notifications
- Integrating with payment gateway
- Advanced customizations

---

**Version:** 1.0  
**Last Updated:** 2024  
**Status:** ✅ Production Ready

# Registration System Implementation Guide

## Overview

A complete user registration and admin approval system has been implemented for the BlackCobra Karate Club. The system requires new members to submit registration with required documents, and admins can approve or reject registrations with payment tracking.

---

## Features Implemented

### 1. **User Registration Page** (`/register/`)
   - Clean, modern registration form with multiple sections
   - **Personal Information Section:**
     - First Name, Last Name
     - Email Address, Phone Number
     - Date of Birth
     - Current Belt Level selection
   
   - **Required Documents Section:**
     - Medical Certificate upload (PDF, DOC, JPG, PNG)
     - Waiver Form upload (PDF, DOC, JPG, PNG)
   
   - **Account Credentials Section:**
     - Password creation with confirmation
     - Form validation for matching passwords
   
   - **Important Payment Alert:**
     - Prominently displays $100 membership fee requirement
     - Notes that payment must be completed before admin approval
     - Clear yellow alert box

### 2. **Registration Model** (`core/models.py`)
   ```python
   class Registration:
       - user (OneToOneField to User)
       - first_name, last_name, email, phone
       - date_of_birth
       - belt_level (white, yellow, orange, green, blue, brown, black)
       - medical_certificate (FileField)
       - waiver (FileField)
       - status (pending, approved, rejected)
       - payment_status (unpaid, paid)
       - membership_fee ($100.00 default)
       - reviewed_by (ForeignKey to admin user)
       - reviewed_at (timestamp)
       - rejection_reason (optional)
       - created_at (timestamp)
   ```

### 3. **Registration Form** (`core/forms.py`)
   - `RegistrationForm` with all validation
   - Password confirmation validation
   - Automatic user account creation on form save
   - Document upload support
   - Styled with Tailwind CSS dark theme

### 4. **Admin User Management** (`/admin/registrations/`)
   
   **Features:**
   - **Registration List View:**
     - Display all registrations with status filters
     - Search by name or email
     - Filter by status (Pending, Approved, Rejected)
     - Filter by payment status (Paid, Unpaid)
     - Statistics cards showing:
       - Pending count
       - Approved count
       - Rejected count
       - Paid count
     - Table with quick action buttons (View, Approve, Reject)
   
   - **Registration Detail View:**
     - Full registration details
     - Personal information display
     - Document download links (Medical Certificate & Waiver)
     - Status and payment information
     - Admin action panel for pending registrations:
       - Checkbox to mark payment as paid
       - "Approve Registration" button
       - Rejection reason textarea
       - "Reject Registration" button
     - Shows review information (who reviewed and when)

### 5. **Admin Sidebar Integration**
   - "User Management" menu item added to admin sidebar
   - Quick access to registration management
   - Active state indication based on current page
   - Positioned right after Dashboard for easy access

---

## File Structure

### Templates Created:
```
templates/
├── auth/
│   └── register.html                  # Registration form page
└── admin/registrations/
    ├── list.html                      # Registration list with filters
    └── detail.html                    # Registration detail & approval
```

### Components Updated:
```
templates/components/
└── sidebar_admin.html                 # Added User Management link
```

### Views Created:
```
core/views/
└── admin_registrations.py             # Registration management views
    - registration_list()
    - registration_detail()
    - registration_approve()
    - registration_reject()
```

### Forms Updated:
```
core/forms.py
├── RegistrationForm                   # New registration form
```

### Models Updated:
```
core/models.py
└── Registration                       # New registration model
```

### URLs Updated:
```
core/urls.py
- path('register/', views.register_view, name='register')
- path('admin/registrations/', admin_reg_views.registration_list, name='admin_registrations')
- path('admin/registrations/<int:registration_id>/', admin_reg_views.registration_detail, name='admin_registration_detail')
- path('admin/registrations/<int:registration_id>/approve/', admin_reg_views.registration_approve, name='admin_registration_approve')
- path('admin/registrations/<int:registration_id>/reject/', admin_reg_views.registration_reject, name='admin_registration_reject')
```

---

## User Flow

### Registration Flow:
1. User navigates to `/register/` or clicks "Create one now" on login page
2. Fills out personal information, uploads documents, creates password
3. Form validates all fields and document uploads
4. System creates User account with unique username from email
5. Registration record created with **pending** status
6. User redirected to login page with success message
7. User receives message about admin approval requirement and payment

### Admin Approval Flow:
1. Admin navigates to `/admin/registrations/`
2. Views list of pending registrations with stats
3. Can search/filter registrations
4. Clicks "View" to see full details
5. Reviews submitted documents (can download)
6. Either:
   - **Approve:** Check payment box if needed, click "Approve Registration"
   - **Reject:** Enter rejection reason, click "Reject Registration"
7. UserProfile is created automatically on approval (role='trainee')
8. User can then log in and access trainee dashboard

---

## Payment Alert Details

### Alert Box Content:
- **Location:** Top of registration form
- **Color:** Yellow (#fbbf24)
- **Icon:** Info icon (!)
- **Message:** "A membership fee of $100.00 is required. Payment must be completed before your account can be activated by an admin."

### Admin Payment Management:
- Registration detail page has checkbox: "Mark as Payment Paid"
- Can be checked during approval process
- Payment status tracked in database
- Lists show payment status for each registration

---

## Key Features

### Security:
- Password confirmation validation
- File upload restrictions (PDF, DOC, DOCX, JPG, PNG only)
- Admin-only access to management pages
- CSRF protection on all forms

### User Experience:
- Clear form sections with icons
- Real-time validation feedback
- Helpful placeholder text
- Dark theme consistent with site
- Mobile-responsive design
- Success/error messages
- Download links for documents

### Admin Experience:
- Quick statistics overview
- Multiple filter options
- Search functionality
- Inline action buttons
- Review tracking (who approved and when)
- Rejection reason storage for record

---

## Database

### Migration:
- Migration file: `core/migrations/0009_registration.py`
- Created Registration table with all fields
- Foreign keys to User and admin user
- File storage in `media/registrations/`

### File Storage:
```
media/
└── registrations/
    ├── medical_certs/      # Medical certificates
    └── waivers/            # Waiver forms
```

---

## Testing the System

### Step 1: Access Registration
```
URL: http://localhost:8000/register/
Or click "Create one now" on login page
```

### Step 2: Submit Registration
1. Fill in all required fields
2. Upload sample documents (PDF/JPG)
3. Create password
4. Click "Create Account & Submit for Review"
5. Redirected to login with success message

### Step 3: Admin Review
1. Log in with admin account
2. Navigate to Admin Dashboard or click "User Management" in sidebar
3. View registrations list with filters
4. Click "View" on a registration
5. Review details and documents
6. Approve or reject with optional reason

### Step 4: Verification
1. New user can log in after approval
2. User's role is 'trainee'
3. User can access trainee dashboard
4. Payment status tracked in admin panel

---

## Customization

### Change Membership Fee:
Edit `core/models.py` Registration model:
```python
membership_fee = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
# Change default value to your amount
```

### Add More Fields to Registration:
1. Add field to Registration model
2. Add to RegistrationForm
3. Add to register.html template
4. Run `python manage.py makemigrations` and `migrate`

### Customize Email on Approval:
Edit `core/views/admin_registrations.py` registration_detail() function to add email sending

### Modify Status Choices:
Edit Registration model STATUS_CHOICES list to add custom statuses

---

## Integration Notes

### With Trainee System:
- On approval, UserProfile is auto-created with role='trainee'
- New trainee can create full profile from trainee dashboard
- Can participate in events immediately after approval

### With Payment System:
- payment_status tracked in Registration
- Admins should verify payment before approval
- Consider integrating with payment gateway for future

### With Notification System:
- Can extend to send notifications on approval/rejection
- Could email users with registration status updates

---

## Commands

### Create Migration:
```bash
python manage.py makemigrations
```

### Apply Migration:
```bash
python manage.py migrate
```

### Check System:
```bash
python manage.py check
```

### Run Development Server:
```bash
python manage.py runserver
```

---

## File Locations

| Component | Location |
|-----------|----------|
| Register View | `core/views/auth.py` |
| Admin Views | `core/views/admin_registrations.py` |
| Registration Form | `core/forms.py` |
| Registration Model | `core/models.py` |
| Register Template | `templates/auth/register.html` |
| Admin List Template | `templates/admin/registrations/list.html` |
| Admin Detail Template | `templates/admin/registrations/detail.html` |
| Admin Sidebar | `templates/components/sidebar_admin.html` |
| URLs | `core/urls.py` |
| Views Init | `core/views/__init__.py` |

---

## Important Notes

1. **File Uploads:** Users must upload medical certificate and waiver as PDF, DOC, DOCX, JPG, or PNG
2. **Username Creation:** System creates username from email (everything before @)
3. **Duplicate Email:** Prevent duplicate emails in User model or add validation
4. **Admin Approval:** Only admins can approve/reject registrations
5. **Payment Tracking:** Payment status must be set before or during approval
6. **User Profile:** Automatically created on approval (role='trainee')
7. **Status Flow:** pending → approved/rejected (no status changes after)

---

## Future Enhancements

1. **Email Notifications:**
   - Send confirmation email on registration
   - Email on approval/rejection

2. **Payment Integration:**
   - Connect to Stripe/PayPal for online payments
   - Track payment receipts
   - Auto-approve on successful payment

3. **Document Review:**
   - Admin notes on documents
   - Request resubmission if documents invalid
   - Expiration date tracking

4. **Automated Workflows:**
   - Auto-reject expired medical certificates
   - Reminder emails for pending approvals
   - Scheduled cleanup of old registrations

5. **Bulk Actions:**
   - Approve multiple registrations at once
   - Bulk export for records
   - CSV import for batch processing

---

## Support

For questions or issues with the registration system:
1. Check the registration form validation
2. Verify file uploads are correct format
3. Ensure admin has proper permissions
4. Check database migration status with `python manage.py showmigrations`
5. Review Django logs for detailed error messages

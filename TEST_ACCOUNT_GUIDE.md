# BlackCobra Karate Club - Test Account Guide

## Overview

Three test user accounts have been created for you to explore the BlackCobra Karate Club management system. Each account has different permissions and access levels based on their role.

## Account Details

### 1️⃣ Administrator Account
**For**: System administration, user management, event management

```
Username: admin_user
Password: Admin@12345
Email:    admin@blackcobra.com
```

**Dashboard Access**: `/admin/dashboard/`

**Features Available**:
- ✅ View all trainees and manage their profiles
- ✅ Create and manage events
- ✅ Create matches and auto-matchmaking
- ✅ Manage judges and assignments
- ✅ Record and track payments
- ✅ Generate reports (membership, financial, event)
- ✅ System statistics and analytics

**Sample Data Included**:
- Phone: +1-234-567-8901
- Address: 123 Dojo Street, Karate City, KC 12345

---

### 2️⃣ Trainee Account
**For**: Students/trainees - personal dashboard and event management

```
Username: trainee_user
Password: Trainee@12345
Email:    trainee@blackcobra.com
```

**Dashboard Access**: `/trainee/dashboard/`

**Features Available**:
- ✅ View personal profile and belt rank
- ✅ Browse and register for events
- ✅ View upcoming matches
- ✅ Check match schedules and competition history
- ✅ View payment history and balance
- ✅ Update personal information

**Sample Data Included**:
- Name: John Trainee
- Phone: +1-345-678-9012
- Address: 456 Martial Road, Fight Town, FT 23456
- Belt Rank: White
- Weight: 70.5 kg
- Status: Active member
- Join Date: ~6 months ago

---

### 3️⃣ Judge Account
**For**: Certified judges - match judging and result entry

```
Username: judge_user
Password: Judge@12345
Email:    judge@blackcobra.com
```

**Dashboard Access**: `/judge/dashboard/`

**Features Available**:
- ✅ View assigned matches
- ✅ View event assignments
- ✅ Record match results
- ✅ Enter scoring details
- ✅ View competition schedule
- ✅ Access judge-specific reports

**Sample Data Included**:
- Name: Master Judge
- Phone: +1-456-789-0123
- Address: 789 Championship Ave, Victory City, VC 34567
- Certification Level: National
- Certification Date: 2010-01-15
- Status: Active

---

## How to Get Started

### Step 1: Create Test Users (Already Done! ✓)
The test users were created by running:
```bash
python manage.py create_test_users
```

### Step 2: Start the Development Server
```bash
python manage.py runserver
```

The server will start at `http://localhost:8000`

### Step 3: View the Landing Page
Visit `http://localhost:8000/` to see:
- Interactive 3D graphics with Three.js
- Feature showcase
- Statistics
- Test credentials modal button

### Step 4: Log In with Test Accounts

**Option A**: Click "Login to Dashboard" or "View Test Credentials" on landing page

**Option B**: Go directly to login page: `http://localhost:8000/login/`

### Step 5: Explore Each Role

#### As Admin (admin_user)
1. View admin dashboard with system statistics
2. Go to Trainees section to see/manage members
3. Check Events section and create new events
4. Explore Matchmaking for tournament setup
5. View Payments and Records
6. Generate Reports

#### As Trainee (trainee_user)
1. View your personal dashboard
2. Go to Events and register for available tournaments
3. Check your upcoming matches
4. Review your payment history
5. View your profile and statistics

#### As Judge (judge_user)
1. View your judge dashboard
2. See assigned matches and events
3. Access results entry for completed matches
4. Review event assignments
5. View judge-specific information

---

## Landing Page Features

### 3D Interactive Graphics
- **Animated 3D Cubes**: Rotating cubes with dynamic lighting
- **Real-time Rendering**: Uses Three.js for GPU-accelerated 3D
- **Responsive Canvas**: Automatically scales to window size
- **Red & Orange Theme**: Brand-colored lighting effects

### Navigation
- **Fixed Top Bar**: Logo, navigation links, and auth buttons
- **Responsive Design**: Works on mobile, tablet, desktop
- **Direct Links**: Quick access to login and dashboards

### Hero Section
- **Full-Screen Canvas**: 3D background with rotating elements
- **Call-to-Action**: "Login to Dashboard" and "View Test Credentials"
- **Statistics**: 500+ members, 50+ trainers, 100+ championships
- **Scroll Indicators**: Visual feedback on page scroll

### Features Section
Six feature cards highlighting:
1. **Expert Instructors** - Certified masters with decades of experience
2. **Competition Ready** - Advanced matchmaking and judging system
3. **Progress Tracking** - Detailed analytics and performance metrics
4. **Community** - Connect with fellow martial artists
5. **Easy Management** - Intuitive dashboard for events and payments
6. **Personalized Training** - Customized plans for each level

### Statistics Section
- 20+ Years of Excellence
- 500+ Active Trainees
- 50+ Certified Instructors
- 1000+ Championships Won

### Test Credentials Modal
Beautiful modal showing all three demo accounts with:
- Username and password for each role
- Description of access levels
- Direct button to login page

---

## Features by Role

### Admin Features ⚙️
```
Dashboard
├── Statistics & Analytics
├── Recent Activity Feed
├── Quick Actions
│
Trainee Management
├── List/Search Trainees
├── Add/Edit/Delete Profiles
├── View Belt Ranks & Status
│
Event Management
├── Create Events
├── Edit Event Details
├── Update Event Status
├── View Registrations
│
Matchmaking
├── Manual Match Creation
├── Auto-Matchmaking
├── Judge Assignments
├── Conflict Validation
│
Payment Management
├── Record Payments
├── Update Status
├── View History
├── Filter by Status
│
Reports
├── Membership Reports
├── Financial Reports
├── Event Reports
├── Export to PDF/CSV
```

### Trainee Features 🥋
```
Dashboard
├── Personal Profile
├── Upcoming Matches
├── Current Events
├── Statistics
│
Events
├── Browse Available Events
├── Register for Events
├── Unregister from Events
├── View Registration Status
│
Matches
├── View Upcoming Matches
├── See Competitor Info
├── Check Match Schedule
├── View Past Results
│
Payments
├── Payment History
├── View Balance
├── Pending Payments
├── Payment Details
```

### Judge Features 🏆
```
Dashboard
├── Judge Profile
├── Certification Info
├── Upcoming Matches Count
│
Events
├── Assigned Events
├── Event Details
├── Participant Info
│
Matches
├── Assigned Matches
├── Competitor Information
├── Match Schedules
├── Status Updates
│
Results
├── Enter Match Results
├── Record Scoring
├── Submit Results
├── View Match History
```

---

## URL Reference

### Public Pages
- `/` - Landing page with 3D graphics
- `/login/` - Login page

### Admin URLs
- `/admin/dashboard/` - Admin dashboard
- `/admin/trainees/` - Trainee management
- `/admin/events/` - Event management
- `/admin/matchmaking/` - Matchmaking system
- `/admin/payments/` - Payment tracking
- `/admin/reports/` - Reports generation

### Trainee URLs
- `/trainee/dashboard/` - Trainee dashboard
- `/trainee/events/` - Event registration
- `/trainee/matches/` - View matches
- `/trainee/payments/` - Payment history

### Judge URLs
- `/judge/dashboard/` - Judge dashboard
- `/judge/events/` - Assigned events
- `/judge/matches/` - Assigned matches
- `/judge/results/` - Results entry

### General
- `/logout/` - Logout (accessible from any authenticated page)

---

## Troubleshooting

### Login Issues
- **Forgot Password?**: No password reset available in test mode. Use the credentials above exactly.
- **Account Disabled?**: Test accounts should be active. Re-run the creation command.
- **Session Expired?**: Log out and log back in.

### 3D Graphics Not Showing
- **Browser Support**: Ensure WebGL is enabled
- **Check Console**: Open browser dev tools to see any errors
- **Try Different Browser**: Test in Chrome, Firefox, or Safari

### Database Issues
- **No Data?**: Run migrations: `python manage.py migrate`
- **Recreate Users?**: Delete and re-run: `python manage.py create_test_users`

### Server Won't Start
```bash
# Different port
python manage.py runserver 8001

# Different host
python manage.py runserver 127.0.0.1:8000
```

---

## Best Practices for Testing

### Testing Admin Features
1. Create a new event as admin
2. Register a trainee (yourself with trainee account)
3. Create matches with auto-matchmaking
4. Assign judges to matches
5. Record payment as admin
6. Generate and export reports

### Testing Trainee Features
1. Browse available events
2. Register for an event
3. Check your matches
4. View match details
5. Review payment history

### Testing Judge Features
1. Check assigned matches
2. View competitor information
3. Enter a match result
4. Review your schedule

### Testing Different Devices
- Mobile: Use browser DevTools device emulation
- Tablet: 768px width
- Desktop: Full screen

---

## Security Notes

⚠️ **Important**: These are test credentials for development only!

- **Never use in production**
- **Change all passwords before going live**
- **Remove test data before deployment**
- **Implement proper authentication in production**
- **Use environment variables for sensitive data**

---

## Support & Documentation

For more information, see:
- `LANDING_PAGE.md` - Technical details
- `LANDING_PAGE_SUMMARY.md` - Implementation overview
- `SETUP_TEST_CREDENTIALS.md` - Setup instructions
- `.kiro/specs/blackcobra-karate-club/tasks.md` - Project roadmap

---

## Quick Command Reference

```bash
# Create test users
python manage.py create_test_users

# Start dev server
python manage.py runserver

# Run migrations
python manage.py migrate

# Django shell (interactive)
python manage.py shell

# Create Django superuser (admin)
python manage.py createsuperuser
```

---

## Next Steps

1. ✅ Create test users (already done)
2. 🔄 Start the dev server
3. 👀 Visit the landing page
4. 🔐 Log in with each test account
5. 🧪 Explore features and test workflows
6. 📝 Review the implementation plan
7. 🚀 Customize for your needs

---

**Enjoy exploring BlackCobra Karate Club Management System!** 🥋

For questions or issues, refer to the documentation files in the project root.

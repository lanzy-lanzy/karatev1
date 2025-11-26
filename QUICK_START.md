# BlackCobra Karate Club - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Create Test Users
```bash
python manage.py create_test_users
```

### Step 2: Start the Server
```bash
python manage.py runserver
```

### Step 3: Visit the Landing Page
Open: `http://localhost:8000/`

---

## 🔐 Test Login Credentials

### Admin Dashboard
```
URL: http://localhost:8000/admin/dashboard/
Username: admin_user
Password: Admin@12345
```

### Trainee Dashboard
```
URL: http://localhost:8000/trainee/dashboard/
Username: trainee_user
Password: Trainee@12345
```

### Judge Dashboard
```
URL: http://localhost:8000/judge/dashboard/
Username: judge_user
Password: Judge@12345
```

---

## ✨ What You'll See

### Landing Page Features
- 🎨 **3D Interactive Graphics** - Rotating cubes powered by Three.js
- 🌙 **Modern Dark Theme** - Professional dark UI with red-orange gradients
- 📱 **Fully Responsive** - Works on mobile, tablet, and desktop
- ⚡ **Smooth Animations** - 60fps animations throughout
- 🔑 **Test Credentials Modal** - Easy access to demo accounts
- 📊 **Statistics Section** - Club achievements and metrics
- ✅ **Feature Showcase** - 6 key platform features

### 3D Canvas Features
- **Rotating Cubes**: 5 animated 3D objects with independent rotations
- **Dynamic Lighting**: Red and orange point lights
- **Interactive**: Canvas responds to window resizing
- **Responsive**: Works on all screen sizes
- **No Dependencies**: Uses Three.js CDN

---

## 📁 Project Structure

```
templates/
├── landing.html ⭐ NEW - Interactive landing page with 3D graphics
├── base.html
└── auth/
    └── login.html

core/
├── views/
│   └── auth.py (updated)
└── management/commands/
    └── create_test_users.py ⭐ NEW - Creates test accounts

Documentation:
├── LANDING_PAGE.md ⭐ - Technical documentation
├── SETUP_TEST_CREDENTIALS.md ⭐ - Setup guide  
├── TEST_ACCOUNT_GUIDE.md ⭐ - Account details
├── LANDING_PAGE_SUMMARY.md ⭐ - Implementation summary
└── QUICK_START.md ⭐ - This file
```

---

## 🎯 What Each Account Can Do

### Admin (admin_user)
- Manage trainees and judges
- Create and manage events
- Set up matches and tournaments
- Record payments
- Generate reports
- View system analytics

### Trainee (trainee_user)
- View personal profile
- Register for events
- Check upcoming matches
- View payment history
- See competition schedules

### Judge (judge_user)
- View assigned matches
- See event assignments
- Record match results
- Track judge schedule

---

## 🎨 Landing Page Highlights

### 1. Navigation Bar
- Fixed top bar with logo
- Navigation links
- Login and Get Started buttons
- Mobile responsive

### 2. Hero Section
- Full-screen with 3D canvas background
- Large headline with gradient text
- Call-to-action buttons
- Live statistics counter
- Scroll indicator dots

### 3. Features Section (6 Cards)
- Expert Instructors
- Competition Ready
- Progress Tracking
- Community
- Easy Management
- Personalized Training

### 4. Statistics Section
- 20+ Years of Excellence
- 500+ Active Trainees
- 50+ Certified Instructors
- 1000+ Championships Won

### 5. Test Credentials Modal
- Beautiful modal popup
- Shows all 3 test accounts
- Username and password display
- Direct login button

### 6. Call-to-Action Section
- Encouragement message
- Dashboard access button
- Demo credentials button

---

## 🔧 Technical Details

### Technologies Used
- **Frontend**: TailwindCSS, AlpineJS, HTML5
- **3D Graphics**: Three.js (via CDN)
- **Backend**: Django
- **Styling**: CSS3 with animations
- **No Build**: Runs with CDN links, no webpack/build step

### Browser Support
- Chrome/Chromium ✅
- Firefox ✅
- Safari ✅
- Edge ✅
- Mobile browsers ✅

### Performance
- Smooth 60fps animations
- Responsive canvas rendering
- Optimized CSS animations
- CDN-based dependencies

---

## 🎮 Testing the 3D Graphics

1. Open DevTools (F12)
2. Check the Console tab for any errors
3. Verify WebGL is enabled:
   - Right-click → Inspect Element → Console
   - Type: `gl = document.getElementById('canvas').getContext('webgl'); gl ? 'WebGL enabled' : 'WebGL disabled'`

If you see **WebGL enabled** ✅, the 3D graphics should work!

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `LANDING_PAGE.md` | Complete technical documentation |
| `SETUP_TEST_CREDENTIALS.md` | Setup instructions & troubleshooting |
| `TEST_ACCOUNT_GUIDE.md` | Detailed account information |
| `LANDING_PAGE_SUMMARY.md` | Implementation overview |
| `QUICK_START.md` | This quick reference |

---

## ⚡ Commands Reference

```bash
# Create test users
python manage.py create_test_users

# Start development server
python manage.py runserver

# Run database migrations
python manage.py migrate

# Access Django shell
python manage.py shell

# Create Django superuser
python manage.py createsuperuser

# Run tests
python manage.py test

# Collect static files
python manage.py collectstatic
```

---

## 🐛 Troubleshooting

### "Module not found" error
```bash
# Install dependencies
pip install -r requirements.txt
```

### Database errors
```bash
# Run migrations
python manage.py migrate
```

### Port 8000 already in use
```bash
# Use different port
python manage.py runserver 8001
```

### 3D graphics not showing
- Check browser WebGL support
- Open DevTools Console and check for errors
- Try a different browser
- Ensure JavaScript is enabled

### Can't log in
- Verify username and password are exact (case-sensitive)
- Ensure test users were created: `python manage.py create_test_users`
- Check if user exists in database

---

## 🔐 Security Reminder

⚠️ These test credentials are **for development only**!

Before production:
- [ ] Remove test user creation command
- [ ] Change all credentials
- [ ] Implement proper authentication
- [ ] Use environment variables
- [ ] Add password hashing
- [ ] Enable HTTPS
- [ ] Disable debug mode

---

## 🎓 Learning Path

1. **Day 1**: Explore landing page and test accounts
2. **Day 2**: Test admin dashboard features
3. **Day 3**: Test trainee features and event registration
4. **Day 4**: Test judge features and match judging
5. **Day 5**: Review reports and analytics

---

## 💡 Next Steps

- ✅ Create test users
- ✅ Start dev server
- ✅ Visit landing page (3D graphics!)
- ✅ Log in with test accounts
- ✅ Explore each role's features
- 📖 Read the detailed documentation
- 🔧 Customize for your needs
- 🚀 Deploy to production

---

## 📞 Support

For detailed help, see:
- `LANDING_PAGE.md` - Technical details
- `TEST_ACCOUNT_GUIDE.md` - Account information
- `SETUP_TEST_CREDENTIALS.md` - Setup help

---

**Ready?** Run these commands:

```bash
python manage.py create_test_users
python manage.py runserver
# Then visit: http://localhost:8000/
```

Enjoy! 🥋

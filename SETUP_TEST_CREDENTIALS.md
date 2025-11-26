# BlackCobra Karate Club - Setup & Test Credentials Guide

## Quick Start

### 1. Create Test Users

Run this command to create test user accounts:

```bash
python manage.py create_test_users
```

### 2. Start the Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000/` to see the landing page.

### 3. Test Credentials

Use these credentials to log in:

#### Admin Account
- **Username**: `admin_user`
- **Password**: `Admin@12345`
- **Access**: Admin Dashboard, User Management, Events, Payments, Reports

#### Trainee Account  
- **Username**: `trainee_user`
- **Password**: `Trainee@12345`
- **Access**: Trainee Dashboard, Event Registration, Matches, Payments

#### Judge Account
- **Username**: `judge_user`
- **Password**: `Judge@12345`
- **Access**: Judge Dashboard, Events, Matches, Results

## Landing Page Features

The landing page includes:

- ✓ **Interactive 3D Graphics** - Rotating 3D cubes using Three.js
- ✓ **Modern UI Design** - Dark theme with red-orange gradients
- ✓ **Responsive Layout** - Mobile, tablet, and desktop views
- ✓ **Smooth Animations** - Float, slide-in, and hover effects
- ✓ **Feature Showcase** - 6 key features with icons
- ✓ **Statistics Section** - Club metrics and achievements
- ✓ **Test Credentials Modal** - Easy access to demo accounts
- ✓ **Glass Morphism Effects** - Frosted glass UI elements

## File Structure

```
templates/
├── landing.html          # New landing page with 3D
├── base.html            # Base template
└── auth/
    └── login.html       # Login page

core/
├── views/
│   └── auth.py          # Updated with landing page view
└── management/
    └── commands/
        └── create_test_users.py  # New management command
```

## Key URLs

- `/` - Landing page (unauthenticated)
- `/login/` - Login page
- `/admin/dashboard/` - Admin dashboard (admin_user)
- `/trainee/dashboard/` - Trainee dashboard (trainee_user)
- `/judge/dashboard/` - Judge dashboard (judge_user)

## Troubleshooting

### Command Not Found
Ensure you're in the project root directory and have activated the Python virtual environment.

### Database Error
Run migrations first:
```bash
python manage.py migrate
```

### Port Already in Use
Use a different port:
```bash
python manage.py runserver 0.0.0.0:8001
```

### WebGL Not Working
Ensure your browser supports WebGL. The landing page gracefully handles browsers without WebGL support.

## Customization

### Update Test Credentials
Edit `core/management/commands/create_test_users.py` to change:
- Usernames
- Passwords
- Email addresses
- Profile information

### Customize Landing Page
Edit `templates/landing.html` to modify:
- Colors (change hex values in CSS)
- Text content (headlines, descriptions)
- 3D animation (canvas rendering code)
- Statistics and features

## Security Notes

**These test credentials are for development only!**

For production:
1. Remove or disable the test credentials modal
2. Create actual user accounts with secure passwords
3. Use Django admin interface for user management
4. Never commit passwords to version control
5. Use environment variables for sensitive data

## Next Steps

1. Explore the admin dashboard with `admin_user`
2. Test trainee features with `trainee_user`
3. Test judge features with `judge_user`
4. Review the implementation plan at `.kiro/specs/blackcobra-karate-club/tasks.md`

# BlackCobra Karate Club - Landing Page & Test Credentials

## Landing Page Features

The new landing page (`templates/landing.html`) provides a visually appealing and interactive introduction to the BlackCobra Karate Club management system.

### Interactive 3D Elements
- **Three.js Integration**: Uses Three.js via CDN to render animated 3D cubes
- **Dynamic Lighting**: Red and orange point lights create a dynamic atmosphere
- **Rotating Objects**: Five 3D cubes rotate at different speeds and directions
- **Responsive Canvas**: Canvas automatically scales to window size

### Visual Design
- **Modern Dark Theme**: Gray-900 background with gradient accents (red-orange)
- **Glass Morphism Effects**: Frosted glass appearance for UI elements
- **Smooth Animations**: 
  - Float animations on CTA buttons
  - Slide-in animations on page load
  - Smooth transitions on card hover effects
  - Pulse ring animations

### Key Sections

1. **Navigation Bar**
   - Fixed top navigation with logo and links
   - Responsive menu with login/get started buttons
   - Glass effect background

2. **Hero Section**
   - Full-screen interactive 3D canvas
   - Large headline with gradient text
   - Call-to-action buttons
   - Live statistics (members, trainers, championships)
   - Scroll indicators

3. **Features Section**
   - 6 feature cards with icons and descriptions:
     - Expert Instructors
     - Competition Ready
     - Progress Tracking
     - Community
     - Easy Management
     - Personalized Training
   - Hover effects with elevation animation

4. **Statistics Section**
   - Key metrics with gradient borders
   - Years of excellence
   - Active trainees
   - Certified instructors
   - Championships won

5. **Call-to-Action Section**
   - Encouraging message
   - Direct link to dashboard
   - Test credentials button

6. **Test Credentials Modal**
   - Beautiful modal displaying demo accounts
   - Three roles with credentials and descriptions
   - Direct link to login page

## Test Credentials

Use these credentials to test the application with different user roles:

### Admin Account
- **Username**: `admin_user`
- **Password**: `Admin@12345`
- **Access**: Full dashboard access, user management, events, reports, payments

### Trainee Account
- **Username**: `trainee_user`
- **Password**: `Trainee@12345`
- **Access**: Personal dashboard, event registration, match information, payment history

### Judge Account
- **Username**: `judge_user`
- **Password**: `Judge@12345`
- **Access**: Judge dashboard, event assignments, match assignments, result entries

## Creating Test Users

To create the test users in your database, run:

```bash
python manage.py create_test_users
```

This command will:
1. Create three test user accounts with the credentials above
2. Set up their user profiles with appropriate roles
3. Create associated Trainee and Judge records where needed
4. Display confirmation with all credentials

## URL Routes

### Landing Page
- **URL**: `/` (home)
- **View**: `home` (shows landing page if not authenticated)
- **Template**: `templates/landing.html`

### Login
- **URL**: `/login/`
- **View**: `login_view`
- **Template**: `templates/auth/login.html`

## Responsive Design

The landing page is fully responsive:
- **Mobile**: Single column layout, hamburger menu integration ready
- **Tablet**: Multi-column feature cards, adjusted typography
- **Desktop**: Full 6-column feature grid, side-by-side CTAs

## Browser Compatibility

- Modern browsers with WebGL support (for Three.js)
- Chrome, Firefox, Safari, Edge
- Graceful degradation if WebGL is unavailable

## Customization

### Colors
Modify the following in the CSS:
- Primary gradient: `#ef4444` (red) to `#f97316` (orange)
- Background: `#111827` (dark gray)
- Accent colors: Various opacity variations

### 3D Elements
Edit the Three.js initialization in the `<script>` section:
- Cube colors, sizes, and rotation speeds
- Lighting positions and intensities
- Camera position and FOV

### Content
Update text in HTML sections for:
- Hero headline and subheadline
- Feature cards
- Statistics
- Company information

## Performance Notes

- Canvas rendering uses requestAnimationFrame for smooth 60fps animation
- Responsive throttling: Canvas resizing uses window resize event
- CSS animations use GPU acceleration (transform, opacity)
- Modal implementation uses vanilla JavaScript with Alpine.js compatible events

## Security Notes

- Test credentials are for development/demo only
- Never use these in production
- Always create unique credentials for production users
- Consider disabling the test credentials modal in production

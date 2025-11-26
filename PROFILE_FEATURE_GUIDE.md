# Trainee Profile Management Feature Guide

## Overview
Trainees can now manage their profile, upload profile pictures, and view their information displayed in match listings.

---

## Feature 1: View Your Profile

### How to Access
- **Method 1**: Click "My Profile" in the left sidebar
- **Method 2**: Click "View Profile" button on the dashboard
- **URL**: `/trainee/profile/`

### What You'll See
```
┌─────────────────────────────────────────────────┐
│  MY PROFILE                                      │
├─────────────────────────────────────────────────┤
│                                                  │
│  [Profile Pic]  Your Full Name                 │
│                 your.email@example.com          │
│                 ⬜ White Belt   🟢 Active       │
│                 ⬜ Lightweight                  │
│                                                  │
│  [Edit Profile] [View Profile Points]          │
│                                                  │
├─────────────────────────────────────────────────┤
│                                                  │
│  CONTACT INFORMATION          TRAINING INFO      │
│  ┌───────────────────┐       ┌──────────────┐  │
│  │ Email: your@ex... │       │ Weight: 65kg │  │
│  │ Phone: +1 555... │       │ Class: Light │  │
│  │ Address: 123...  │       │ DoB: Jan 1.. │  │
│  └───────────────────┘       └──────────────┘  │
│                                                  │
│  EMERGENCY CONTACT            PERFORMANCE       │
│  ┌───────────────────┐       ┌──────────────┐  │
│  │ Contact: John Doe │       │ Points: 250  │  │
│  │ Phone: +1 555...  │       │ Wins: 8      │  │
│  └───────────────────┘       │ Losses: 2    │  │
│                              │ Events: 3    │  │
│                              └──────────────┘  │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## Feature 2: Edit Your Profile

### How to Access
- **Method 1**: Click "Edit Profile" button on dashboard
- **Method 2**: Click "Edit Profile" button on your profile page
- **URL**: `/trainee/profile/edit/`

### Profile Picture Upload Section
```
┌─────────────────────────────────────────────────┐
│  PROFILE PICTURE                                │
│  Upload a clear, professional photo             │
├─────────────────────────────────────────────────┤
│                                                  │
│  [Current Picture]    Choose Picture            │
│                       [Browse Files...]         │
│   Current picture     JPG, PNG or GIF (5MB max)│
│                                                  │
│                       [Select Picture...]       │
│                                                  │
└─────────────────────────────────────────────────┘
```

### Personal Information Section
```
┌─────────────────────────────────────────────────┐
│  PERSONAL INFORMATION                           │
├─────────────────────────────────────────────────┤
│                                                  │
│  [John      ] [Doe              ]               │
│   First Name    Last Name                       │
│                                                  │
│  [john@example.com                    ]         │
│   Email Address                                 │
│                                                  │
│  [+1 (555) 123-4567             ]              │
│   Phone Number                                  │
│                                                  │
│  [1990-01-15              ]                    │
│   Date of Birth                                 │
│                                                  │
│  [123 Main Street, City, State, ZIP]           │
│  [Apt 4B                              ]         │
│   Address (multiple lines)                      │
│                                                  │
└─────────────────────────────────────────────────┘
```

### Training Information Section
```
┌─────────────────────────────────────────────────┐
│  TRAINING INFORMATION                           │
├─────────────────────────────────────────────────┤
│                                                  │
│  [65.5       ]                                 │
│   Weight (kg) - Auto-calculates weight class   │
│                                                  │
│  [John Doe                    ]                │
│   Emergency Contact Name                        │
│                                                  │
│  [+1 (555) 987-6543          ]                │
│   Emergency Contact Phone                       │
│                                                  │
└─────────────────────────────────────────────────┘
```

### Form Actions
```
[Cancel]                                [Save Changes]
```

---

## Feature 3: Profile Pictures in Matches

### Upcoming Matches View
```
┌─────────────────────────────────────────────────────────┐
│  UPCOMING MATCHES                                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  [Picture1]  John vs Mary  [Picture2]                  │
│   Blue Bdry  White Black   Red Border                  │
│   Border     Belt          Belt                         │
│                                                          │
│  Event: Tournament 2025                                │
│  Date & Time: Dec 15, 2024 2:00 PM                    │
│  Location: Main Dojo                                  │
│                                                          │
│  Status: Scheduled                                     │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Past Matches View
```
┌─────────────────────────────────────────────────────────┐
│  PAST MATCHES                                           │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  [Picture1]  John vs Mary  [Picture2]                  │
│   Green      White Black   Gray Border                 │
│   Border     Belt          Belt                         │
│   WINNER     You           LOSER                       │
│                                                          │
│  Event: Tournament 2024                                │
│  Date: Dec 10, 2024                                    │
│  Location: Main Dojo                                   │
│                                                          │
│  Result: Won ✓                                        │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Picture Display Behavior
```
Profile Picture Uploaded:        Profile Picture NOT Uploaded:
┌─────────┐                      ┌──────┐
│ Real    │                      │ J.D. │  (Initials)
│ Picture │                      │      │
│         │                      │      │
└─────────┘                      └──────┘
```

---

## Step-by-Step: Upload Your Profile Picture

### Step 1: Go to Edit Profile
```
Dashboard → [Edit Profile] button
     OR
My Profile → [Edit Profile] button
```

### Step 2: Upload Picture
```
1. Scroll to "PROFILE PICTURE" section
2. Click [Choose Picture] button
3. Select image from your computer
4. Click [Open] to confirm selection
5. See preview update with new image
```

### Step 3: Update Other Information (Optional)
```
1. Update First Name / Last Name
2. Update Email Address
3. Update Phone Number
4. Update Date of Birth
5. Update Address
6. Update Weight (auto-calculates class)
7. Update Emergency Contact Name
8. Update Emergency Contact Phone
```

### Step 4: Save Changes
```
1. Click [Save Changes] button
2. Wait for processing...
3. See success message
4. Redirected to your profile
5. View changes immediately
```

---

## Supported Image Formats

| Format | Extension | Maximum Size | Quality |
|--------|-----------|--------------|---------|
| JPEG   | .jpg      | 5 MB         | Excellent |
| PNG    | .png      | 5 MB         | Excellent |
| GIF    | .gif      | 5 MB         | Good |

**Recommended**: JPEG or PNG format, 500x500 pixels or larger

---

## Best Practices for Profile Pictures

### ✓ DO:
- Use clear, well-lit headshot
- Face clearly visible
- Professional appearance
- Natural colors
- Square or near-square image
- Show chest/shoulders
- Friendly expression
- Recent photo (last 1-2 years)

### ✗ DON'T:
- Use blurry or poor quality images
- Group photos with multiple people
- Cover your face with objects
- Use overly dark or bright images
- Use cartoon/meme images
- Use completely off-topic images
- Use very old photos
- Use heavily filtered images

### Example Good Picture:
```
   [Professional headshot]
   - Clear face
   - Good lighting
   - Friendly expression
   - Natural background
   - Recent photo
```

---

## Troubleshooting

### Issue: Picture won't upload
**Solutions:**
- [ ] Check file is actually an image (JPG, PNG, GIF)
- [ ] Check file size is under 5 MB
- [ ] Try different file format
- [ ] Try different browser
- [ ] Clear browser cache (Ctrl+Shift+Del)
- [ ] Check internet connection stable

### Issue: Picture not showing in matches
**Solutions:**
- [ ] Upload picture first (profile edit page)
- [ ] Refresh page (F5 or Cmd+R)
- [ ] Clear browser cache
- [ ] Wait 1-2 minutes for updates to propagate
- [ ] Check image uploaded successfully
- [ ] Try different browser

### Issue: Can't see Edit Profile button
**Solutions:**
- [ ] Check you're logged in as trainee
- [ ] Go directly to `/trainee/profile/edit/`
- [ ] Try clicking "My Profile" in sidebar first
- [ ] Log out and log in again
- [ ] Try different browser

### Issue: Changes not saving
**Solutions:**
- [ ] Check all required fields filled
- [ ] Check error messages (shown in red)
- [ ] Verify internet connection
- [ ] Try again
- [ ] Clear form and start over
- [ ] Contact administrator if persists

---

## Profile Information Privacy

### Who Can See Your Profile?
| Information | Trainees | Judges | Admin |
|------------|----------|--------|-------|
| Profile Picture | Yes | Yes | Yes |
| Name | Yes | Yes | Yes |
| Belt Rank | Yes | Yes | Yes |
| Weight Class | Yes | Yes | Yes |
| Phone | No | No | Yes |
| Email | No | No | Yes |
| Address | No | No | Yes |
| DOB | No | No | Yes |
| Emergency Contact | No | No | Yes |

---

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Go to Profile | Alt + P |
| Go to Edit Profile | Alt + E |
| Save Form | Ctrl + S |
| Refresh Page | F5 / Cmd + R |

---

## Performance Tips

1. **Upload Optimization**
   - Resize large images before uploading
   - Compress images for faster upload
   - Use JPEG format for photos

2. **Viewing Optimization**
   - Clear browser cache regularly
   - Close unused browser tabs
   - Use modern browser for best performance

3. **Storage**
   - Keep only current profile picture
   - Old pictures automatically replaced
   - No storage limit for normal use

---

## FAQ

**Q: Can I upload multiple pictures?**
A: No, only one profile picture per trainee. Uploading a new picture replaces the old one.

**Q: What if I don't upload a picture?**
A: Your initials (first letter of first and last name) will display instead.

**Q: Can I delete my profile picture?**
A: Edit profile and don't upload a new picture. The field will remain empty.

**Q: Who can see my profile picture?**
A: Visible to you, other trainees, judges, and administrators.

**Q: Can I use a logo or team picture?**
A: No, profile pictures should be personal headshots for identification in matches.

**Q: How often can I change my picture?**
A: Anytime! Update your profile whenever you want.

**Q: Is my personal info secure?**
A: Yes, protected by login authentication and secure database.

**Q: Can I export my profile data?**
A: Contact your administrator for data export requests.

---

## Contact & Support

If you have questions or issues:
1. Check this guide first
2. Ask your instructor
3. Contact system administrator
4. Submit support ticket through system

---

Last Updated: November 27, 2025

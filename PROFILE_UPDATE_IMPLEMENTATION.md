# Trainee Profile Update & Profile Picture Implementation

## Overview
This implementation adds the ability for trainees to view and update their profiles, including uploading a profile picture that is displayed in match views.

## Features Implemented

### 1. Profile Management
- **View Profile**: Display comprehensive trainee profile information
- **Edit Profile**: Update personal information including:
  - First name and last name
  - Email address
  - Phone number
  - Date of birth
  - Address
  - Weight (auto-calculates weight class)
  - Emergency contact name and phone
  - Profile picture upload

### 2. Profile Picture Upload
- Image upload support for profile pictures
- Automatic image validation
- Pictures displayed with fallback initials if no image uploaded
- Supported formats: JPG, PNG, GIF

### 3. Match Display Enhancement
- Profile pictures now displayed in upcoming matches
- Profile pictures displayed in past match results
- Visual indicators for winners (green border/background)
- Fallback to initials if no profile picture exists

### 4. Dashboard Integration
- Added "View Profile" and "Edit Profile" buttons to trainee dashboard
- Quick access to profile management features

## Files Created

### Backend
1. **core/forms.py** (NEW)
   - `TraineeProfileForm`: Form for updating user profile information
   - `TraineeDetailForm`: Form for updating trainee-specific information

### Frontend Templates
1. **templates/trainee/profile.html** (NEW)
   - Displays complete trainee profile
   - Shows personal, training, emergency contact, and performance information
   - Links to edit profile

2. **templates/trainee/profile_edit.html** (NEW)
   - Form for editing profile information
   - Profile picture upload interface
   - Organized sections for personal and training information
   - Form validation and error messages

### Updated Files
1. **core/views/trainee.py**
   - Added imports for forms
   - Added `profile_view()` - displays trainee profile
   - Added `profile_edit()` - handles profile updates with POST/GET

2. **core/urls.py**
   - Added route: `trainee/profile/` → `profile_view`
   - Added route: `trainee/profile/edit/` → `profile_edit`

3. **templates/trainee/dashboard.html**
   - Added "View Profile" and "Edit Profile" buttons
   - Profile picture already existed, now properly linked

4. **templates/trainee/matches.html**
   - Updated upcoming matches to display profile pictures
   - Updated past matches to display profile pictures
   - Added fallback avatars with initials
   - Added visual indicators for winners (green border)

## Database Schema

The implementation uses the existing `UserProfile` model which already includes:
```python
profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
```

No database migrations are required as the field already exists.

## URL Routes

```
/trainee/profile/             - View trainee profile
/trainee/profile/edit/        - Edit trainee profile and upload picture
```

## Usage

### For Trainees

1. **View Profile**
   - Click "View Profile" button on dashboard
   - See complete profile information including:
     - Profile picture
     - Personal details
     - Training information
     - Emergency contact
     - Performance statistics

2. **Edit Profile**
   - Click "Edit Profile" button on dashboard or profile view
   - Upload or change profile picture
   - Update personal information
   - Update training information
   - Save changes

3. **View Profile Pictures in Matches**
   - Navigate to "Matches" page
   - See profile pictures for upcoming matches
   - See profile pictures for past match results
   - Winners shown with green border indicator

### Form Validation

The profile forms include validation for:
- Email format validation
- Phone number format
- Weight as decimal number
- Date of birth as valid date
- File upload validation (image files only)

## File Upload Configuration

**Location**: `media/profiles/`
**Settings**: Already configured in `karate/settings.py`
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

## Template Features

### Profile Display
- Responsive design (mobile and desktop)
- Color-coded belt rank badges
- Status badges (Active/Inactive/Suspended)
- Organized information cards
- Quick access to edit functionality

### Profile Edit Form
- Multi-step form organization
- Clear section headers
- Inline form validation errors
- File upload preview
- Cancel and save options

### Match Display
- Professional profile picture display
- Fallback to initials avatar
- Color-coded borders (blue for upcoming, green for winners)
- Responsive card layout
- Touch-friendly for mobile devices

## Security Considerations

1. **Access Control**
   - All profile views protected by `@trainee_required` decorator
   - Trainees can only edit their own profile
   - Form validates ownership before processing

2. **File Upload**
   - Only image files accepted
   - Upload path restricted to `profiles/` directory
   - File size validation (max 5MB recommended)

3. **Data Privacy**
   - Profile information visible to trainee and admin
   - Email and phone fields optional for privacy

## Error Handling

The profile edit view handles:
- Form validation errors with user-friendly messages
- File upload errors
- Database save errors
- Concurrent edit conflicts

## Testing Recommendations

1. **Profile Upload**
   - Test with various image formats (JPG, PNG, GIF)
   - Test with large files
   - Test with invalid file types

2. **Form Validation**
   - Test with invalid email format
   - Test with empty required fields
   - Test with special characters in text fields

3. **Display**
   - Verify profile pictures appear in:
     - Profile view
     - Dashboard
     - Upcoming matches
     - Past match results
   - Test fallback initials display when no image

4. **Cross-browser**
   - Test image upload in different browsers
   - Test responsive design on mobile devices

## Performance Considerations

1. **Image Optimization**
   - Recommend compressing images before upload
   - Consider implementing automatic image resizing
   - Cache profile images in browser

2. **Database Queries**
   - Profile views use related_name for efficient queries
   - Matches view uses select_related for profile pictures
   - No N+1 query problems

## Future Enhancements

1. **Image Processing**
   - Automatic image resizing
   - Image cropping tool
   - Multiple image formats support

2. **Profile Features**
   - Profile bio/bio field
   - Achievement badges
   - Training statistics graphs
   - Profile visibility settings

3. **Social Features**
   - Public profile page
   - Follow/friend system
   - Profile sharing

## Troubleshooting

### Profile pictures not displaying
- Check `MEDIA_ROOT` and `MEDIA_URL` settings in settings.py
- Verify `media/` directory exists and is writable
- Check file permissions on uploaded images
- Clear browser cache

### Form not submitting
- Check CSRF token is included in form
- Verify `enctype="multipart/form-data"` on form element
- Check form validation errors in console

### Image upload fails
- Verify file is actually an image
- Check file size is under limit
- Verify `Pillow` library is installed for image handling

## Dependencies

The implementation requires:
- Django (existing)
- Pillow (for image handling) - already installed based on ImageField usage

## Code Examples

### Uploading a Profile Picture

```html
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    <input type="file" name="profile_image" accept="image/*">
    <button type="submit">Upload</button>
</form>
```

### Displaying Profile Picture

```html
{% if trainee.profile.profile_image %}
    <img src="{{ trainee.profile.profile_image.url }}" alt="Profile">
{% else %}
    <div class="avatar">{{ initials }}</div>
{% endif %}
```

### Accessing in Views

```python
trainee = get_object_or_404(Trainee, profile__user=request.user)
profile_image = trainee.profile.profile_image
```

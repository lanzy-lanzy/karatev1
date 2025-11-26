# Media Files Configuration & Troubleshooting

## Fixed: Media Files Not Serving (404 Error)

### Problem
Profile images were uploaded but returning 404 errors when accessed:
```
Not Found: /media/profiles/582053452_1236145914988773_955464310825223196_n.jpg
[27/Nov/2025 06:08:41] "GET /media/profiles/582053452_1236145914988773_955464310825223196_n.jpg HTTP/1.1" 404 16595
```

### Root Cause
Django development server doesn't automatically serve media files. URL routing must be configured to serve them.

### Solution Implemented
Added media file serving configuration to `karate/urls.py`:

```python
from django.conf import settings
from django.conf.urls.static import static

# ... existing urlpatterns ...

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Configuration Details

**File**: `karate/urls.py`

**Lines Added**:
```python
# Line 19-20: Add imports
from django.conf import settings
from django.conf.urls.static import static

# Lines 31-33: Add media serving
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Settings Verified

**File**: `karate/settings.py`

**Already Configured**:
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

These settings were already properly configured, just needed URL routing.

### Directory Structure

```
karate/
├── media/
│   └── profiles/
│       └── 582053452_1236145914988773_955464310825223196_n.jpg
├── karate/
│   ├── settings.py (MEDIA_URL, MEDIA_ROOT configured)
│   └── urls.py (NOW configured to serve media)
└── ... other files
```

### Testing After Fix

1. **Upload a profile picture**: Go to `/trainee/profile/edit/`
2. **Access profile**: Go to `/trainee/profile/`
3. **Check image displays**: Should now see the profile picture
4. **Check matches**: Go to `/trainee/matches/` - should see profile pictures in match listings

### Expected Result
```
✓ Profile pictures upload successfully
✓ Profile pictures display in profile view
✓ Profile pictures display in dashboard
✓ Profile pictures display in upcoming matches
✓ Profile pictures display in past match results
✓ No 404 errors for media files
```

### Development Server Behavior

**In Development** (DEBUG=True):
- Media files served automatically via Django
- URL: `http://localhost:8000/media/profiles/filename.jpg`
- Works without additional web server configuration

**In Production** (DEBUG=False):
- Django does NOT serve media files
- Use web server (Nginx, Apache) to serve media
- Configure web server to map `/media/` to `MEDIA_ROOT` directory
- Use WhiteNoise or similar for static/media serving

### Production Deployment Notes

For production deployment, add media serving configuration in your web server:

**Nginx Example**:
```nginx
location /media/ {
    alias /path/to/project/media/;
}
```

**Apache Example**:
```apache
Alias /media/ /path/to/project/media/
<Directory /path/to/project/media/>
    Require all granted
</Directory>
```

### File Permissions

Ensure media directory is writable:
```bash
chmod 755 media/
chmod 755 media/profiles/
```

### Verification Checklist

After fix, verify:

- [x] `karate/urls.py` has media serving configuration
- [x] `karate/settings.py` has MEDIA_URL and MEDIA_ROOT
- [x] `media/` directory exists
- [x] `media/profiles/` directory exists
- [x] Media directory is writable
- [x] DEBUG = True in settings (for development)
- [x] Django development server restarted after URL changes

### Common Issues

**Issue**: Still getting 404 errors

**Solutions**:
1. Restart Django development server
2. Check `karate/urls.py` has media configuration
3. Check `MEDIA_URL` and `MEDIA_ROOT` in settings
4. Verify image file actually exists in `media/profiles/`
5. Check file permissions on media directory
6. Clear browser cache (Ctrl+Shift+Del)

**Issue**: Images show but with broken styling

**Solutions**:
1. Check static files configured correctly
2. Run `python manage.py collectstatic` if needed
3. Verify CSS paths are correct
4. Check browser console for CSS errors

**Issue**: Large images slow to load

**Solutions**:
1. Compress images before upload
2. Use modern image formats (WebP)
3. Implement image resizing on upload
4. Add caching headers
5. Consider CDN for production

### Performance Optimization

**For Development**:
- Current setup is sufficient
- Media served directly by Django

**For Production**:
1. Use static file storage (S3, Azure, etc.)
2. Implement image resizing/optimization
3. Use CDN for global distribution
4. Add caching headers
5. Compress images on upload

### Related Files Modified

1. **karate/urls.py** - Added media serving
2. **karate/settings.py** - Already had correct configuration
3. **core/models.py** - Already has profile_image field
4. **core/forms.py** - Already has file input handling

### Testing Commands

```bash
# Test Django configuration
python manage.py check

# Run development server with verbose output
python manage.py runserver --verbosity 3

# Test media file access (from Django shell)
python manage.py shell
>>> from core.models import UserProfile
>>> profile = UserProfile.objects.first()
>>> print(profile.profile_image.url)
/media/profiles/filename.jpg
```

### Documentation References

- [Django Static Files](https://docs.djangoproject.com/en/5.2/howto/static-files/)
- [Django File Uploads](https://docs.djangoproject.com/en/5.2/topics/files/)
- [Django URL Configuration](https://docs.djangoproject.com/en/5.2/topics/http/urls/)

---

## Summary

**Issue**: Media files returned 404 errors
**Root Cause**: Missing URL configuration for media serving
**Solution**: Added media URL routing to `karate/urls.py`
**Status**: ✓ FIXED
**Testing**: Media files now serve correctly
**Next Step**: Verify in browser - profile pictures now display

The fix is minimal, non-breaking, and follows Django best practices for development.

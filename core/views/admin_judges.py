"""
Judge Management Views for Admin.
Handles judge creation, editing, deletion, and listing.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from core.models import Judge, UserProfile
from .admin import admin_required


@admin_required
def judge_list(request):
    """
    List all active judges with search and filter capabilities.
    """
    judges = Judge.objects.filter(is_active=True).select_related('profile__user').order_by('profile__user__first_name', 'profile__user__last_name')
    
    # Apply search filter
    search = request.GET.get('search', '').strip()
    if search:
        judges = judges.filter(
            Q(profile__user__first_name__icontains=search) |
            Q(profile__user__last_name__icontains=search) |
            Q(profile__user__username__icontains=search) |
            Q(profile__user__email__icontains=search)
        )
    
    # Apply certification level filter
    certification = request.GET.get('certification', '').strip()
    if certification:
        judges = judges.filter(certification_level=certification)
    
    context = {
        'judges': judges,
        'certification_levels': Judge._meta.get_field('certification_level').choices,
    }
    
    # Return partial for HTMX requests
    if request.headers.get('HX-Request'):
        return render(request, 'admin/judges/list_partial.html', context)
    
    return render(request, 'admin/judges/list.html', context)


@admin_required
def judge_list_partial(request):
    """
    Partial view for HTMX judge list updates.
    """
    judges = Judge.objects.filter(is_active=True).select_related('profile__user').order_by('profile__user__first_name', 'profile__user__last_name')
    
    # Apply search filter
    search = request.GET.get('search', '').strip()
    if search:
        judges = judges.filter(
            Q(profile__user__first_name__icontains=search) |
            Q(profile__user__last_name__icontains=search) |
            Q(profile__user__username__icontains=search) |
            Q(profile__user__email__icontains=search)
        )
    
    # Apply certification level filter
    certification = request.GET.get('certification', '').strip()
    if certification:
        judges = judges.filter(certification_level=certification)
    
    context = {
        'judges': judges,
        'certification_levels': Judge._meta.get_field('certification_level').choices,
    }
    
    return render(request, 'admin/judges/list_partial.html', context)


@admin_required
def archived_judges_list(request):
    """
    List all archived judges with search and filter capabilities.
    """
    judges = Judge.objects.filter(is_active=False).select_related('profile__user').order_by('-profile__user__first_name')
    
    # Apply search filter
    search = request.GET.get('search', '').strip()
    if search:
        judges = judges.filter(
            Q(profile__user__first_name__icontains=search) |
            Q(profile__user__last_name__icontains=search) |
            Q(profile__user__username__icontains=search)
        )
    
    context = {
        'judges': judges,
        'certification_levels': Judge._meta.get_field('certification_level').choices,
    }
    
    # Return partial for HTMX requests
    if request.headers.get('HX-Request'):
        return render(request, 'admin/judges/archived_partial.html', context)
    
    return render(request, 'admin/judges/archived.html', context)


@admin_required
def archived_judges_list_partial(request):
    """
    Partial view for HTMX archived judges list updates.
    """
    judges = Judge.objects.filter(is_active=False).select_related('profile__user').order_by('-profile__user__first_name')
    
    # Apply search filter
    search = request.GET.get('search', '').strip()
    if search:
        judges = judges.filter(
            Q(profile__user__first_name__icontains=search) |
            Q(profile__user__last_name__icontains=search) |
            Q(profile__user__username__icontains=search)
        )
    
    context = {
        'judges': judges,
        'certification_levels': Judge._meta.get_field('certification_level').choices,
    }
    
    return render(request, 'admin/judges/archived_partial.html', context)


@admin_required
def judge_add(request):
    """
    Add new judge view.
    """
    if request.method == 'POST':
        # User information
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        username = request.POST.get('username', '').strip()
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        # Judge information
        certification_level = request.POST.get('certification_level', '').strip()
        certification_date = request.POST.get('certification_date', '').strip()
        
        errors = {}
        
        # Validation
        if not first_name:
            errors['first_name'] = 'First name is required'
        if not last_name:
            errors['last_name'] = 'Last name is required'
        if not email:
            errors['email'] = 'Email is required'
        elif User.objects.filter(email=email).exists():
            errors['email'] = 'Email already exists'
        if not username:
            errors['username'] = 'Username is required'
        elif User.objects.filter(username=username).exists():
            errors['username'] = 'Username already exists'
        if not password:
            errors['password'] = 'Password is required'
        elif len(password) < 8:
            errors['password'] = 'Password must be at least 8 characters long'
        elif password != confirm_password:
            errors['confirm_password'] = 'Passwords do not match'
        if not certification_level:
            errors['certification_level'] = 'Certification level is required'
        if not certification_date:
            errors['certification_date'] = 'Certification date is required'
        
        if errors:
            form_data = {
                'first_name': {'value': first_name, 'errors': [errors.get('first_name')] if errors.get('first_name') else []},
                'last_name': {'value': last_name, 'errors': [errors.get('last_name')] if errors.get('last_name') else []},
                'email': {'value': email, 'errors': [errors.get('email')] if errors.get('email') else []},
                'username': {'value': username, 'errors': [errors.get('username')] if errors.get('username') else []},
                'phone': {'value': phone, 'errors': []},
                'password': {'value': '', 'errors': [errors.get('password')] if errors.get('password') else []},
                'confirm_password': {'value': '', 'errors': [errors.get('confirm_password')] if errors.get('confirm_password') else []},
                'certification_level': {'value': certification_level, 'errors': [errors.get('certification_level')] if errors.get('certification_level') else []},
                'certification_date': {'value': certification_date, 'errors': [errors.get('certification_date')] if errors.get('certification_date') else []},
            }
            return render(request, 'admin/judges/form.html', {
                'form': form_data,
                'certification_levels': Judge._meta.get_field('certification_level').choices,
            })
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        
        # Create user profile
        profile = UserProfile.objects.create(
            user=user,
            role='judge',
            phone=phone,
        )
        
        # Create judge record
        Judge.objects.create(
            profile=profile,
            certification_level=certification_level,
            certification_date=certification_date,
            is_active=True,
        )
        
        messages.success(request, f'Judge {first_name} {last_name} has been created successfully.')
        
        if request.headers.get('HX-Request'):
            response = HttpResponse()
            response['HX-Redirect'] = '/admin/judges/'
            return response
        
        return redirect('admin_judges')
    
    return render(request, 'admin/judges/form.html', {
        'form': {},
        'certification_levels': Judge._meta.get_field('certification_level').choices,
    })


@admin_required
def judge_edit(request, judge_id):
    """
    Edit judge view.
    """
    judge = get_object_or_404(Judge, id=judge_id)
    
    if request.method == 'POST':
        # User information
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        
        # Judge information
        certification_level = request.POST.get('certification_level', '').strip()
        certification_date = request.POST.get('certification_date', '').strip()
        is_active = request.POST.get('is_active') == 'on'
        
        errors = {}
        
        # Validation
        if not first_name:
            errors['first_name'] = 'First name is required'
        if not last_name:
            errors['last_name'] = 'Last name is required'
        if not email:
            errors['email'] = 'Email is required'
        elif User.objects.filter(email=email).exclude(id=judge.profile.user.id).exists():
            errors['email'] = 'Email already exists'
        if not certification_level:
            errors['certification_level'] = 'Certification level is required'
        if not certification_date:
            errors['certification_date'] = 'Certification date is required'
        
        if errors:
            form_data = {
                'first_name': {'value': first_name, 'errors': [errors.get('first_name')] if errors.get('first_name') else []},
                'last_name': {'value': last_name, 'errors': [errors.get('last_name')] if errors.get('last_name') else []},
                'email': {'value': email, 'errors': [errors.get('email')] if errors.get('email') else []},
                'phone': {'value': phone, 'errors': []},
                'certification_level': {'value': certification_level, 'errors': [errors.get('certification_level')] if errors.get('certification_level') else []},
                'certification_date': {'value': certification_date, 'errors': [errors.get('certification_date')] if errors.get('certification_date') else []},
                'is_active': {'value': is_active, 'errors': []},
            }
            return render(request, 'admin/judges/form.html', {
                'form': form_data,
                'judge': judge,
                'certification_levels': Judge._meta.get_field('certification_level').choices,
            })
        
        # Update user
        judge.profile.user.first_name = first_name
        judge.profile.user.last_name = last_name
        judge.profile.user.email = email
        judge.profile.user.save()
        
        # Update profile
        judge.profile.phone = phone
        judge.profile.save()
        
        # Update judge
        judge.certification_level = certification_level
        judge.certification_date = certification_date
        judge.is_active = is_active
        judge.save()
        
        messages.success(request, f'Judge {first_name} {last_name} has been updated successfully.')
        
        if request.headers.get('HX-Request'):
            response = HttpResponse()
            response['HX-Redirect'] = '/admin/judges/'
            return response
        
        return redirect('admin_judges')
    
    form_data = {
        'first_name': {'value': judge.profile.user.first_name},
        'last_name': {'value': judge.profile.user.last_name},
        'email': {'value': judge.profile.user.email},
        'phone': {'value': judge.profile.phone},
        'certification_level': {'value': judge.certification_level},
        'certification_date': {'value': judge.certification_date.isoformat() if judge.certification_date else ''},
        'is_active': {'value': judge.is_active},
    }
    
    return render(request, 'admin/judges/form.html', {
        'form': form_data,
        'judge': judge,
        'certification_levels': Judge._meta.get_field('certification_level').choices,
    })


@admin_required
def judge_deactivate(request, judge_id):
    """
    Deactivate (archive) a judge.
    """
    judge = get_object_or_404(Judge, id=judge_id)
    judge_name = judge.profile.user.get_full_name() or judge.profile.user.username
    
    if request.method == 'POST':
        judge.is_active = False
        judge.save()
        
        messages.success(request, f'Judge "{judge_name}" has been deactivated.')
        
        if request.headers.get('HX-Request'):
            response = HttpResponse()
            response['HX-Redirect'] = '/admin/judges/'
            return response
        
        return redirect('admin_judges')
    
    return redirect('admin_judges')


@admin_required
def judge_restore(request, judge_id):
    """
    Restore (reactivate) a judge.
    """
    judge = get_object_or_404(Judge, id=judge_id)
    judge_name = judge.profile.user.get_full_name() or judge.profile.user.username
    
    if request.method == 'POST':
        judge.is_active = True
        judge.save()
        
        messages.success(request, f'Judge "{judge_name}" has been reactivated.')
        
        if request.headers.get('HX-Request'):
            response = HttpResponse()
            response['HX-Redirect'] = '/admin/judges/archived/'
            return response
        
        return redirect('admin_archived_judges')
    
    return redirect('admin_archived_judges')

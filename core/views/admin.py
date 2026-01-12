"""
Admin views for the BlackCobra Karate Club System.
Handles admin dashboard and management functionality.
"""
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import timedelta

from core.decorators import admin_required
from core.models import Trainee, UserProfile, Event, EventRegistration, Payment, Match, MatchResult, BeltRankProgress, Registration


@admin_required
def dashboard_view(request):
    """
    Admin dashboard view displaying key metrics and recent activity.
    Requirements: 2.1, 2.2, 2.3
    """
    # Get current date for queries
    now = timezone.now()
    
    # Metric 1: Total trainee count
    total_trainees = Trainee.objects.count()
    
    # Metric 2: Active events count
    active_events = Event.objects.filter(status__in=['open', 'ongoing']).count()
    
    # Metric 3: Pending payments count
    pending_payments = Payment.objects.filter(status='pending').count()
    
    # Metric 4: Upcoming matches count
    upcoming_matches = Match.objects.filter(status='scheduled', scheduled_time__gte=now).count()
    
    # Recent activity feed
    recent_activity = get_recent_activity()
    
    context = {
        'total_trainees': total_trainees,
        'active_events': active_events,
        'pending_payments': pending_payments,
        'upcoming_matches': upcoming_matches,
        'recent_activity': recent_activity,
    }
    
    return render(request, 'admin/dashboard.html', context)


def get_recent_activity(limit=10):
    """
    Get recent activity feed showing latest registrations, payments, and match results.
    Requirements: 2.2
    
    Returns a list of activity items sorted by date (most recent first).
    Each activity item contains:
    - type: 'registration', 'payment', or 'match_result'
    - icon: icon identifier for the frontend
    - message: human-readable description
    - date: date/datetime of the activity
    - color: color theme for the activity type
    """
    activities = []
    
    # Get recent trainee registrations
    activities.extend(get_recent_registrations(limit))
    
    # Get recent payments
    activities.extend(get_recent_payments(limit))
    
    # Get recent match results
    activities.extend(get_recent_match_results(limit))
    
    # Sort by date (most recent first)
    # Handle both date and datetime objects by converting to timezone-aware datetime
    from datetime import datetime
    def get_comparable_date(activity):
        date_val = activity['date']
        if isinstance(date_val, datetime):
            # Already a datetime, ensure it's timezone-aware
            if timezone.is_naive(date_val):
                return timezone.make_aware(date_val)
            return date_val
        else:
            # Convert date to timezone-aware datetime (start of day)
            naive_dt = datetime.combine(date_val, datetime.min.time())
            return timezone.make_aware(naive_dt)
    
    activities.sort(key=get_comparable_date, reverse=True)
    
    return activities[:limit]


def get_recent_registrations(limit=10):
    """
    Get recent trainee registrations for the activity feed.
    Requirements: 2.2
    """
    activities = []
    
    recent_trainees = Trainee.objects.select_related(
        'profile__user'
    ).order_by('-joined_date')[:limit]
    
    for trainee in recent_trainees:
        name = trainee.profile.user.get_full_name() or trainee.profile.user.username
        activities.append({
            'type': 'registration',
            'icon': 'user-plus',
            'message': f"New trainee registered: {name}",
            'date': trainee.joined_date,
            'color': 'green',
        })
    
    return activities


def get_recent_payments(limit=10):
    """
    Get recent payments for the activity feed.
    Requirements: 2.2
    """
    activities = []
    
    recent_payments = Payment.objects.select_related(
        'trainee__profile__user'
    ).order_by('-payment_date')[:limit]
    
    for payment in recent_payments:
        name = payment.trainee.profile.user.get_full_name() or payment.trainee.profile.user.username
        activities.append({
            'type': 'payment',
            'icon': 'currency-dollar',
            'message': f"Payment received from {name}: ${payment.amount}",
            'date': payment.payment_date,
            'color': 'blue',
        })
    
    return activities


def get_recent_match_results(limit=10):
    """
    Get recent match results for the activity feed.
    Requirements: 2.2
    """
    activities = []
    
    recent_results = MatchResult.objects.select_related(
        'match__competitor1__profile__user',
        'match__competitor2__profile__user',
        'winner__profile__user'
    ).order_by('-submitted_at')[:limit]
    
    for result in recent_results:
        winner_name = result.winner.profile.user.get_full_name() or result.winner.profile.user.username
        activities.append({
            'type': 'match_result',
            'icon': 'trophy',
            'message': f"Match completed: {winner_name} won",
            'date': result.submitted_at,
            'color': 'purple',
        })
    
    return activities


# Trainee Management Views
# Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6

@admin_required
def trainee_list(request):
    """
    Trainee list view with search and filter functionality.
    Requirements: 3.1, 3.6
    """
    trainees = Trainee.objects.select_related('profile__user').filter(archived=False)
    
    # Apply search filter
    search = request.GET.get('search', '').strip()
    if search:
        trainees = trainees.filter(
            Q(profile__user__first_name__icontains=search) |
            Q(profile__user__last_name__icontains=search) |
            Q(profile__user__username__icontains=search) |
            Q(belt_rank__icontains=search) |
            Q(status__icontains=search)
        )
    
    # Apply status filter
    status_filter = request.GET.get('status_filter', '').strip()
    if status_filter:
        trainees = trainees.filter(status=status_filter)
    
    # Apply belt filter
    belt_filter = request.GET.get('belt_filter', '').strip()
    if belt_filter:
        trainees = trainees.filter(belt_rank=belt_filter)
    
    # Order by name
    trainees = trainees.order_by('profile__user__first_name', 'profile__user__last_name')
    
    context = {'trainees': trainees}
    
    # Return partial for HTMX requests
    if request.headers.get('HX-Request'):
        return render(request, 'admin/trainees/list_partial.html', context)
    
    return render(request, 'admin/trainees/list.html', context)


@admin_required
def trainee_list_partial(request):
    """
    Partial view for HTMX trainee list updates.
    Requirements: 3.6
    """
    trainees = Trainee.objects.select_related('profile__user').filter(archived=False)
    
    # Apply search filter
    search = request.GET.get('search', '').strip()
    if search:
        trainees = trainees.filter(
            Q(profile__user__first_name__icontains=search) |
            Q(profile__user__last_name__icontains=search) |
            Q(profile__user__username__icontains=search) |
            Q(belt_rank__icontains=search) |
            Q(status__icontains=search)
        )
    
    # Apply status filter
    status_filter = request.GET.get('status_filter', '').strip()
    if status_filter:
        trainees = trainees.filter(status=status_filter)
    
    # Apply belt filter
    belt_filter = request.GET.get('belt_filter', '').strip()
    if belt_filter:
        trainees = trainees.filter(belt_rank=belt_filter)
    
    # Order by name
    trainees = trainees.order_by('profile__user__first_name', 'profile__user__last_name')
    
    return render(request, 'admin/trainees/list_partial.html', {'trainees': trainees})


@admin_required
def trainee_add(request):
    """
    Add new trainee view.
    Requirements: 3.2, 3.3
    """
    if request.method == 'POST':
        # Extract form data
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        date_of_birth = request.POST.get('date_of_birth', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        belt_rank = request.POST.get('belt_rank', '').strip()
        weight = request.POST.get('weight', '').strip()
        status = request.POST.get('status', 'active').strip()
        emergency_contact = request.POST.get('emergency_contact', '').strip()
        emergency_phone = request.POST.get('emergency_phone', '').strip()
        
        # Validation
        errors = {}
        if not first_name:
            errors['first_name'] = 'First name is required'
        if not last_name:
            errors['last_name'] = 'Last name is required'
        if not email:
            errors['email'] = 'Email is required'
        elif User.objects.filter(email=email).exists():
            errors['email'] = 'A user with this email already exists'
        if not date_of_birth:
            errors['date_of_birth'] = 'Date of birth is required'
        if not belt_rank:
            errors['belt_rank'] = 'Belt rank is required'
        if not weight:
            errors['weight'] = 'Weight is required'
        if not emergency_contact:
            errors['emergency_contact'] = 'Emergency contact name is required'
        if not emergency_phone:
            errors['emergency_phone'] = 'Emergency contact phone is required'
        
        if errors:
            # Return form with errors
            form_data = {
                'first_name': {'value': first_name, 'errors': [errors.get('first_name')] if errors.get('first_name') else []},
                'last_name': {'value': last_name, 'errors': [errors.get('last_name')] if errors.get('last_name') else []},
                'email': {'value': email, 'errors': [errors.get('email')] if errors.get('email') else []},
                'date_of_birth': {'value': date_of_birth, 'errors': [errors.get('date_of_birth')] if errors.get('date_of_birth') else []},
                'phone': {'value': phone, 'errors': []},
                'address': {'value': address, 'errors': []},
                'belt_rank': {'value': belt_rank, 'errors': [errors.get('belt_rank')] if errors.get('belt_rank') else []},
                'weight': {'value': weight, 'errors': [errors.get('weight')] if errors.get('weight') else []},
                'status': {'value': status, 'errors': []},
                'emergency_contact': {'value': emergency_contact, 'errors': [errors.get('emergency_contact')] if errors.get('emergency_contact') else []},
                'emergency_phone': {'value': emergency_phone, 'errors': [errors.get('emergency_phone')] if errors.get('emergency_phone') else []},
            }
            return render(request, 'admin/trainees/form.html', {'form': form_data})
        
        # Create user
        username = f"{first_name.lower()}.{last_name.lower()}"
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password='changeme123'  # Default password, should be changed
        )
        
        # Create profile
        profile = UserProfile.objects.create(
            user=user,
            role='trainee',
            phone=phone,
            address=address,
            date_of_birth=date_of_birth
        )
        
        # Create trainee
        Trainee.objects.create(
            profile=profile,
            belt_rank=belt_rank,
            weight=weight,
            emergency_contact=emergency_contact,
            emergency_phone=emergency_phone,
            status=status
        )
        
        messages.success(request, f'Trainee {first_name} {last_name} has been added successfully.')
        
        # For HTMX requests, redirect with HX-Redirect header
        if request.headers.get('HX-Request'):
            response = HttpResponse()
            response['HX-Redirect'] = '/admin/trainees/'
            return response
        
        return redirect('admin_trainees')
    
    # GET request - show empty form
    return render(request, 'admin/trainees/form.html', {'form': {}})


@admin_required
def trainee_edit(request, trainee_id):
    """
    Edit trainee view.
    Requirements: 3.4
    """
    trainee = get_object_or_404(Trainee.objects.select_related('profile__user'), id=trainee_id)
    
    if request.method == 'POST':
        # Extract form data
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        date_of_birth = request.POST.get('date_of_birth', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        belt_rank = request.POST.get('belt_rank', '').strip()
        weight = request.POST.get('weight', '').strip()
        status = request.POST.get('status', 'active').strip()
        emergency_contact = request.POST.get('emergency_contact', '').strip()
        emergency_phone = request.POST.get('emergency_phone', '').strip()
        
        # Validation
        errors = {}
        if not first_name:
            errors['first_name'] = 'First name is required'
        if not last_name:
            errors['last_name'] = 'Last name is required'
        if not email:
            errors['email'] = 'Email is required'
        elif User.objects.filter(email=email).exclude(id=trainee.profile.user.id).exists():
            errors['email'] = 'A user with this email already exists'
        if not date_of_birth:
            errors['date_of_birth'] = 'Date of birth is required'
        if not belt_rank:
            errors['belt_rank'] = 'Belt rank is required'
        if not weight:
            errors['weight'] = 'Weight is required'
        if not emergency_contact:
            errors['emergency_contact'] = 'Emergency contact name is required'
        if not emergency_phone:
            errors['emergency_phone'] = 'Emergency contact phone is required'
        
        if errors:
            # Return form with errors
            form_data = {
                'first_name': {'value': first_name, 'errors': [errors.get('first_name')] if errors.get('first_name') else []},
                'last_name': {'value': last_name, 'errors': [errors.get('last_name')] if errors.get('last_name') else []},
                'email': {'value': email, 'errors': [errors.get('email')] if errors.get('email') else []},
                'date_of_birth': {'value': date_of_birth, 'errors': [errors.get('date_of_birth')] if errors.get('date_of_birth') else []},
                'phone': {'value': phone, 'errors': []},
                'address': {'value': address, 'errors': []},
                'belt_rank': {'value': belt_rank, 'errors': [errors.get('belt_rank')] if errors.get('belt_rank') else []},
                'weight': {'value': weight, 'errors': [errors.get('weight')] if errors.get('weight') else []},
                'status': {'value': status, 'errors': []},
                'emergency_contact': {'value': emergency_contact, 'errors': [errors.get('emergency_contact')] if errors.get('emergency_contact') else []},
                'emergency_phone': {'value': emergency_phone, 'errors': [errors.get('emergency_phone')] if errors.get('emergency_phone') else []},
            }
            return render(request, 'admin/trainees/form.html', {'form': form_data, 'trainee': trainee})
        
        # Update user
        user = trainee.profile.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        
        # Update profile
        profile = trainee.profile
        profile.phone = phone
        profile.address = address
        profile.date_of_birth = date_of_birth
        profile.save()
        
        # Update trainee
        trainee.belt_rank = belt_rank
        trainee.weight = weight
        trainee.status = status
        trainee.emergency_contact = emergency_contact
        trainee.emergency_phone = emergency_phone
        trainee.save()
        
        messages.success(request, f'Trainee {first_name} {last_name} has been updated successfully.')
        
        # For HTMX requests, redirect with HX-Redirect header
        if request.headers.get('HX-Request'):
            response = HttpResponse()
            response['HX-Redirect'] = '/admin/trainees/'
            return response
        
        return redirect('admin_trainees')
    
    # GET request - show form with existing data
    form_data = {
        'first_name': {'value': trainee.profile.user.first_name, 'errors': []},
        'last_name': {'value': trainee.profile.user.last_name, 'errors': []},
        'email': {'value': trainee.profile.user.email, 'errors': []},
        'date_of_birth': {'value': trainee.profile.date_of_birth.isoformat() if trainee.profile.date_of_birth else '', 'errors': []},
        'phone': {'value': trainee.profile.phone, 'errors': []},
        'address': {'value': trainee.profile.address, 'errors': []},
        'belt_rank': {'value': trainee.belt_rank, 'errors': []},
        'weight': {'value': trainee.weight, 'errors': []},
        'status': {'value': trainee.status, 'errors': []},
        'emergency_contact': {'value': trainee.emergency_contact, 'errors': []},
        'emergency_phone': {'value': trainee.emergency_phone, 'errors': []},
    }
    return render(request, 'admin/trainees/form.html', {'form': form_data, 'trainee': trainee})


@admin_required
def trainee_delete(request, trainee_id):
    """
    Archive trainee view (soft delete).
    Requirements: 3.5
    """
    trainee = get_object_or_404(Trainee.objects.select_related('profile__user'), id=trainee_id, archived=False)
    
    if request.method == 'DELETE' or request.method == 'POST':
        user = trainee.profile.user
        trainee_name = user.get_full_name() or user.username
        
        # Archive trainee instead of deleting
        trainee.archived = True
        trainee.save()
        
        # For HTMX requests, return updated list
        if request.headers.get('HX-Request'):
            trainees = Trainee.objects.select_related('profile__user').filter(archived=False).order_by(
                'profile__user__first_name', 'profile__user__last_name'
            )
            response = render(request, 'admin/trainees/list_partial.html', {'trainees': trainees})
            response['HX-Trigger'] = json.dumps({
                'showToast': {'message': f'Trainee {trainee_name} has been archived.', 'type': 'success'}
            })
            return response
        
        messages.success(request, f'Trainee {trainee_name} has been archived.')
        return redirect('admin_trainees')
    
    return redirect('admin_trainees')


@admin_required
def archived_trainees_list(request):
    """
    Archived trainees list view with search and filter functionality.
    Requirements: 3.1
    """
    trainees = Trainee.objects.select_related('profile__user').filter(archived=True)
    
    # Apply search filter
    search = request.GET.get('search', '').strip()
    if search:
        trainees = trainees.filter(
            Q(profile__user__first_name__icontains=search) |
            Q(profile__user__last_name__icontains=search) |
            Q(profile__user__username__icontains=search) |
            Q(belt_rank__icontains=search) |
            Q(status__icontains=search)
        )
    
    # Apply status filter
    status_filter = request.GET.get('status_filter', '').strip()
    if status_filter:
        trainees = trainees.filter(status=status_filter)
    
    # Apply belt filter
    belt_filter = request.GET.get('belt_filter', '').strip()
    if belt_filter:
        trainees = trainees.filter(belt_rank=belt_filter)
    
    # Order by name
    trainees = trainees.order_by('profile__user__first_name', 'profile__user__last_name')
    
    context = {'trainees': trainees}
    
    # Return partial for HTMX requests
    if request.headers.get('HX-Request'):
        return render(request, 'admin/trainees/archived_partial.html', context)
    
    return render(request, 'admin/trainees/archived.html', context)


@admin_required
def archived_trainees_list_partial(request):
    """
    Partial view for HTMX archived trainees list updates.
    Requirements: 3.6
    """
    trainees = Trainee.objects.select_related('profile__user').filter(archived=True)
    
    # Apply search filter
    search = request.GET.get('search', '').strip()
    if search:
        trainees = trainees.filter(
            Q(profile__user__first_name__icontains=search) |
            Q(profile__user__last_name__icontains=search) |
            Q(profile__user__username__icontains=search) |
            Q(belt_rank__icontains=search) |
            Q(status__icontains=search)
        )
    
    # Apply status filter
    status_filter = request.GET.get('status_filter', '').strip()
    if status_filter:
        trainees = trainees.filter(status=status_filter)
    
    # Apply belt filter
    belt_filter = request.GET.get('belt_filter', '').strip()
    if belt_filter:
        trainees = trainees.filter(belt_rank=belt_filter)
    
    # Order by name
    trainees = trainees.order_by('profile__user__first_name', 'profile__user__last_name')
    
    from django.middleware.csrf import get_token
    csrf_token = get_token(request)
    
    return render(request, 'admin/trainees/archived_partial.html', {'trainees': trainees, 'csrf_token': csrf_token})


@admin_required
def trainee_restore(request, trainee_id):
    """
    Restore archived trainee view.
    Requirements: 3.5
    """
    trainee = get_object_or_404(Trainee.objects.select_related('profile__user'), id=trainee_id, archived=True)
    
    if request.method == 'POST':
        user = trainee.profile.user
        trainee_name = user.get_full_name() or user.username
        trainee.archived = False
        trainee.save()
        
        if request.headers.get('HX-Request'):
            from django.middleware.csrf import get_token
            csrf_token = get_token(request)
            trainees = Trainee.objects.select_related('profile__user').filter(archived=True).order_by(
                'profile__user__first_name', 'profile__user__last_name'
            )
            response = render(request, 'admin/trainees/archived_partial.html', {'trainees': trainees, 'csrf_token': csrf_token})
            response['HX-Trigger'] = json.dumps({
                'showToast': {'message': f'Trainee {trainee_name} has been restored.', 'type': 'success'}
            })
            return response
        
        messages.success(request, f'Trainee {trainee_name} has been restored.')
        return redirect('admin_archived_trainees')
    
    return redirect('admin_archived_trainees')


# Event Management Views
# Requirements: 4.1, 4.2, 4.3, 4.4, 4.5

@admin_required
def event_list(request):
    """
    Event list view with search and filter functionality.
    Requirements: 4.1
    """
    events = Event.objects.filter(archived=False)
    
    # Apply search filter
    search = request.GET.get('search', '').strip()
    if search:
        events = events.filter(
            Q(name__icontains=search) |
            Q(location__icontains=search)
        )
    
    # Apply status filter
    status_filter = request.GET.get('status_filter', '').strip()
    if status_filter:
        events = events.filter(status=status_filter)
    
    # Order by event date (upcoming first)
    events = events.order_by('-event_date')
    
    context = {'events': events}
    
    # Return partial for HTMX requests
    if request.headers.get('HX-Request'):
        return render(request, 'admin/events/list_partial.html', context)
    
    return render(request, 'admin/events/list.html', context)


@admin_required
def event_list_partial(request):
    """
    Partial view for HTMX event list updates.
    Requirements: 4.1
    """
    events = Event.objects.filter(archived=False)
    
    # Apply search filter
    search = request.GET.get('search', '').strip()
    if search:
        events = events.filter(
            Q(name__icontains=search) |
            Q(location__icontains=search)
        )
    
    # Apply status filter
    status_filter = request.GET.get('status_filter', '').strip()
    if status_filter:
        events = events.filter(status=status_filter)
    
    # Order by event date
    events = events.order_by('-event_date')
    
    from django.middleware.csrf import get_token
    csrf_token = get_token(request)
    
    return render(request, 'admin/events/list_partial.html', {'events': events, 'csrf_token': csrf_token})


@admin_required
def event_detail(request, event_id):
    """
    Event detail view showing participants, judges, and matches.
    Requirements: 4.4
    """
    event = get_object_or_404(Event, id=event_id)
    
    # Get registered participants
    registrations = event.registrations.filter(status='registered').select_related(
        'trainee__profile__user'
    ).order_by('registered_at')
    
    # Get matches for this event (when Match model exists)
    matches = []
    try:
        from core.models import Match
        matches = Match.objects.filter(event=event).select_related(
            'competitor1__profile__user',
            'competitor2__profile__user'
        ).order_by('scheduled_time')
    except (ImportError, Exception):
        pass
    
    context = {
        'event': event,
        'registrations': registrations,
        'matches': matches,
    }
    
    return render(request, 'admin/events/detail.html', context)


@admin_required
def event_add(request):
    """
    Add new event view.
    Requirements: 4.2, 4.3
    """
    if request.method == 'POST':
        # Extract form data
        name = request.POST.get('name', '').strip()
        event_date = request.POST.get('event_date', '').strip()
        location = request.POST.get('location', '').strip()
        description = request.POST.get('description', '').strip()
        registration_deadline = request.POST.get('registration_deadline', '').strip()
        max_participants = request.POST.get('max_participants', '').strip()
        status = request.POST.get('status', 'draft').strip()
        
        # Validation
        errors = {}
        if not name:
            errors['name'] = 'Event name is required'
        if not event_date:
            errors['event_date'] = 'Event date is required'
        if not location:
            errors['location'] = 'Location is required'
        if not registration_deadline:
            errors['registration_deadline'] = 'Registration deadline is required'
        if not max_participants:
            errors['max_participants'] = 'Maximum participants is required'
        else:
            try:
                max_participants = int(max_participants)
                if max_participants < 1:
                    errors['max_participants'] = 'Maximum participants must be at least 1'
            except ValueError:
                errors['max_participants'] = 'Maximum participants must be a number'
        
        if errors:
            form_data = {
                'name': {'value': name, 'errors': [errors.get('name')] if errors.get('name') else []},
                'event_date': {'value': event_date, 'errors': [errors.get('event_date')] if errors.get('event_date') else []},
                'location': {'value': location, 'errors': [errors.get('location')] if errors.get('location') else []},
                'description': {'value': description, 'errors': []},
                'registration_deadline': {'value': registration_deadline, 'errors': [errors.get('registration_deadline')] if errors.get('registration_deadline') else []},
                'max_participants': {'value': max_participants if isinstance(max_participants, str) else str(max_participants), 'errors': [errors.get('max_participants')] if errors.get('max_participants') else []},
                'status': {'value': status, 'errors': []},
            }
            return render(request, 'admin/events/form.html', {'form': form_data})
        
        # Create event
        event = Event.objects.create(
            name=name,
            event_date=event_date,
            location=location,
            description=description,
            registration_deadline=registration_deadline,
            max_participants=max_participants,
            status=status
        )
        
        # Check if event should be auto-closed on creation
        if status == 'open':
            closure_reason = event.close_registration()
            if closure_reason:
                if closure_reason == 'registration_deadline_passed':
                    messages.warning(request, f'Event "{name}" has been created but registration is already closed (deadline has passed).')
                elif closure_reason == 'max_participants_reached':
                    messages.warning(request, f'Event "{name}" has been created but registration is already closed (max participants reached).')
                else:
                    messages.success(request, f'Event "{name}" has been created successfully.')
            else:
                messages.success(request, f'Event "{name}" has been created successfully.')
        else:
            messages.success(request, f'Event "{name}" has been created successfully.')
        
        if request.headers.get('HX-Request'):
            response = HttpResponse()
            response['HX-Redirect'] = '/admin/events/'
            return response
        
        return redirect('admin_events')
    
    return render(request, 'admin/events/form.html', {'form': {}})


@admin_required
def event_edit(request, event_id):
    """
    Edit event view.
    Requirements: 4.2, 4.3
    """
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        # Extract form data
        name = request.POST.get('name', '').strip()
        event_date = request.POST.get('event_date', '').strip()
        location = request.POST.get('location', '').strip()
        description = request.POST.get('description', '').strip()
        registration_deadline = request.POST.get('registration_deadline', '').strip()
        max_participants = request.POST.get('max_participants', '').strip()
        status = request.POST.get('status', 'draft').strip()
        
        # Validation
        errors = {}
        if not name:
            errors['name'] = 'Event name is required'
        if not event_date:
            errors['event_date'] = 'Event date is required'
        if not location:
            errors['location'] = 'Location is required'
        if not registration_deadline:
            errors['registration_deadline'] = 'Registration deadline is required'
        if not max_participants:
            errors['max_participants'] = 'Maximum participants is required'
        else:
            try:
                max_participants = int(max_participants)
                if max_participants < 1:
                    errors['max_participants'] = 'Maximum participants must be at least 1'
            except ValueError:
                errors['max_participants'] = 'Maximum participants must be a number'
        
        if errors:
            form_data = {
                'name': {'value': name, 'errors': [errors.get('name')] if errors.get('name') else []},
                'event_date': {'value': event_date, 'errors': [errors.get('event_date')] if errors.get('event_date') else []},
                'location': {'value': location, 'errors': [errors.get('location')] if errors.get('location') else []},
                'description': {'value': description, 'errors': []},
                'registration_deadline': {'value': registration_deadline, 'errors': [errors.get('registration_deadline')] if errors.get('registration_deadline') else []},
                'max_participants': {'value': max_participants if isinstance(max_participants, str) else str(max_participants), 'errors': [errors.get('max_participants')] if errors.get('max_participants') else []},
                'status': {'value': status, 'errors': []},
            }
            return render(request, 'admin/events/form.html', {'form': form_data, 'event': event})
        
        # Update event
        event.name = name
        event.event_date = event_date
        event.location = location
        event.description = description
        event.registration_deadline = registration_deadline
        event.max_participants = max_participants
        event.status = status
        event.save()
        
        # Check if event should be auto-closed
        if status == 'open':
            closure_reason = event.close_registration()
            if closure_reason:
                if closure_reason == 'registration_deadline_passed':
                    messages.warning(request, f'Event "{name}" has been updated and registration has been automatically closed due to deadline.')
                elif closure_reason == 'max_participants_reached':
                    messages.warning(request, f'Event "{name}" has been updated and registration has been automatically closed - maximum participants reached.')
                else:
                    messages.success(request, f'Event "{name}" has been updated successfully.')
            else:
                messages.success(request, f'Event "{name}" has been updated successfully.')
        else:
            messages.success(request, f'Event "{name}" has been updated successfully.')
        
        if request.headers.get('HX-Request'):
            response = HttpResponse()
            response['HX-Redirect'] = '/admin/events/'
            return response
        
        return redirect('admin_events')
    
    # GET request - show form with existing data
    form_data = {
        'name': {'value': event.name, 'errors': []},
        'event_date': {'value': event.event_date.isoformat() if event.event_date else '', 'errors': []},
        'location': {'value': event.location, 'errors': []},
        'description': {'value': event.description, 'errors': []},
        'registration_deadline': {'value': event.registration_deadline.isoformat() if event.registration_deadline else '', 'errors': []},
        'max_participants': {'value': event.max_participants, 'errors': []},
        'status': {'value': event.status, 'errors': []},
    }
    return render(request, 'admin/events/form.html', {'form': form_data, 'event': event})


@admin_required
def event_archive(request, event_id):
    """
    Archive event view.
    Requirements: 4.3
    """
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        event_name = event.name
        event.archived = True
        event.save()
        
        if request.headers.get('HX-Request'):
            from django.middleware.csrf import get_token
            csrf_token = get_token(request)
            events = Event.objects.filter(archived=False).order_by('-event_date')
            response = render(request, 'admin/events/list_partial.html', {'events': events, 'csrf_token': csrf_token})
            response['HX-Trigger'] = json.dumps({
                'showToast': {'message': f'Event "{event_name}" has been archived.', 'type': 'success'}
            })
            return response
        
        messages.success(request, f'Event "{event_name}" has been archived.')
        return redirect('admin_events')
    
    return redirect('admin_events')


@admin_required
def archived_events_list(request):
    """
    Archived events list view with search and filter functionality.
    Requirements: 4.1
    """
    events = Event.objects.filter(archived=True)
    
    # Apply search filter
    search = request.GET.get('search', '').strip()
    if search:
        events = events.filter(
            Q(name__icontains=search) |
            Q(location__icontains=search)
        )
    
    # Apply status filter
    status_filter = request.GET.get('status_filter', '').strip()
    if status_filter:
        events = events.filter(status=status_filter)
    
    # Order by event date (most recent first)
    events = events.order_by('-event_date')
    
    context = {'events': events}
    
    # Return partial for HTMX requests
    if request.headers.get('HX-Request'):
        return render(request, 'admin/events/archived_partial.html', context)
    
    return render(request, 'admin/events/archived.html', context)


@admin_required
def archived_events_list_partial(request):
    """
    Partial view for HTMX archived events list updates.
    Requirements: 4.1
    """
    events = Event.objects.filter(archived=True)
    
    # Apply search filter
    search = request.GET.get('search', '').strip()
    if search:
        events = events.filter(
            Q(name__icontains=search) |
            Q(location__icontains=search)
        )
    
    # Apply status filter
    status_filter = request.GET.get('status_filter', '').strip()
    if status_filter:
        events = events.filter(status=status_filter)
    
    # Order by event date
    events = events.order_by('-event_date')
    
    from django.middleware.csrf import get_token
    csrf_token = get_token(request)
    
    return render(request, 'admin/events/archived_partial.html', {'events': events, 'csrf_token': csrf_token})


@admin_required
def event_restore(request, event_id):
    """
    Restore archived event view.
    Requirements: 4.3
    """
    event = get_object_or_404(Event, id=event_id, archived=True)
    
    if request.method == 'POST':
        event_name = event.name
        event.archived = False
        event.save()
        
        if request.headers.get('HX-Request'):
            from django.middleware.csrf import get_token
            csrf_token = get_token(request)
            events = Event.objects.filter(archived=True).order_by('-event_date')
            response = render(request, 'admin/events/archived_partial.html', {'events': events, 'csrf_token': csrf_token})
            response['HX-Trigger'] = json.dumps({
                'showToast': {'message': f'Event "{event_name}" has been restored.', 'type': 'success'}
            })
            return response
        
        messages.success(request, f'Event "{event_name}" has been restored.')
        return redirect('admin_archived_events')
    
    return redirect('admin_archived_events')


@admin_required
def event_status_update(request, event_id):
    """
    Update event status via HTMX without page reload.
    Requirements: 4.5
    """
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status', '').strip()
        
        # Validate status
        valid_statuses = [choice[0] for choice in Event.STATUS_CHOICES]
        if new_status in valid_statuses:
            old_status = event.status
            event.status = new_status
            event.save()
            
            # Return updated status badge for HTMX
            if request.headers.get('HX-Request'):
                response = render(request, 'admin/events/status_badge.html', {'event': event})
                response['HX-Trigger'] = json.dumps({
                    'showToast': {
                        'message': f'Event status updated to "{event.get_status_display()}"',
                        'type': 'success'
                    }
                })
                return response
        else:
            if request.headers.get('HX-Request'):
                response = render(request, 'admin/events/status_badge.html', {'event': event})
                response['HX-Trigger'] = json.dumps({
                    'showToast': {
                        'message': 'Invalid status value',
                        'type': 'error'
                    }
                })
                return response
    
    return redirect('admin_event_detail', event_id=event_id)


@admin_required
def matchmaking_list(request):
    """
    Matchmaking list view displaying all matches grouped by event.
    Requirements: 5.1
    """
    from core.models import Match, Event, Judge
    
    # Get all events with matches
    events = Event.objects.prefetch_related(
        'matches__competitor1__profile__user',
        'matches__competitor2__profile__user',
        'matches__judge_assignments__judge__profile__user'
    ).order_by('-event_date')
    
    # Apply event filter
    event_filter = request.GET.get('event_filter', '').strip()
    if event_filter:
        events = events.filter(id=event_filter)
    
    # Apply status filter
    status_filter = request.GET.get('status_filter', '').strip()
    
    # Build event data with matches
    events_with_matches = []
    for event in events:
        matches = event.matches.filter(archived=False)
        if status_filter:
            matches = matches.filter(status=status_filter)
        matches = matches.order_by('-created_at')
        
        if matches.exists() or not event_filter:
            events_with_matches.append({
                'event': event,
                'matches': matches
            })
    
    # Get all events for filter dropdown
    all_events = Event.objects.all().order_by('-event_date')
    
    # Get all judges for the form
    judges = Judge.objects.filter(is_active=True).select_related('profile__user')
    
    context = {
        'events_with_matches': events_with_matches,
        'all_events': all_events,
        'judges': judges,
    }
    
    if request.headers.get('HX-Request'):
        return render(request, 'admin/matchmaking/list_partial.html', context)
    
    return render(request, 'admin/matchmaking/list.html', context)


@admin_required
def matchmaking_list_partial(request):
    """
    Partial view for HTMX matchmaking list updates.
    Requirements: 5.1
    """
    from core.models import Match, Event, Judge
    
    events = Event.objects.prefetch_related(
        'matches__competitor1__profile__user',
        'matches__competitor2__profile__user',
        'matches__judge_assignments__judge__profile__user'
    ).order_by('-event_date')
    
    event_filter = request.GET.get('event_filter', '').strip()
    if event_filter:
        events = events.filter(id=event_filter)
    
    status_filter = request.GET.get('status_filter', '').strip()
    
    events_with_matches = []
    for event in events:
        matches = event.matches.filter(archived=False)
        if status_filter:
            matches = matches.filter(status=status_filter)
        matches = matches.order_by('-created_at')
        
        if matches.exists() or not event_filter:
            events_with_matches.append({
                'event': event,
                'matches': matches
            })
    
    return render(request, 'admin/matchmaking/list_partial.html', {'events_with_matches': events_with_matches})


@admin_required
def match_add(request):
    """
    Add new match view.
    Requirements: 5.2
    """
    from core.models import Match, MatchJudge, Event, Trainee, Judge, EventRegistration
    
    if request.method == 'POST':
        event_id = request.POST.get('event', '').strip()
        competitor1_id = request.POST.get('competitor1', '').strip()
        competitor2_id = request.POST.get('competitor2', '').strip()
        scheduled_time = request.POST.get('scheduled_time', '').strip()
        judge_ids = request.POST.getlist('judges')
        notes = request.POST.get('notes', '').strip()
        match_type = request.POST.get('match_type', 'sparring').strip()
        
        errors = {}
        if not event_id:
            errors['event'] = 'Event is required'
        if not competitor1_id:
            errors['competitor1'] = 'Competitor 1 is required'
        if not competitor2_id:
            errors['competitor2'] = 'Competitor 2 is required'
        if competitor1_id and competitor2_id and competitor1_id == competitor2_id:
            errors['competitor2'] = 'Competitors must be different'
        if not scheduled_time:
            errors['scheduled_time'] = 'Scheduled time is required'
        if len([j for j in judge_ids if j]) < 3:
            errors['judges'] = 'At least 3 judges must be selected'
        
        if errors:
            events = Event.objects.filter(status__in=['open', 'closed', 'ongoing']).order_by('-event_date')
            trainees = Trainee.objects.filter(status='active').select_related('profile__user')
            judges = Judge.objects.filter(is_active=True).select_related('profile__user')
            
            form_data = {
                'event': {'value': event_id, 'errors': [errors.get('event')] if errors.get('event') else []},
                'competitor1': {'value': competitor1_id, 'errors': [errors.get('competitor1')] if errors.get('competitor1') else []},
                'competitor2': {'value': competitor2_id, 'errors': [errors.get('competitor2')] if errors.get('competitor2') else []},
                'scheduled_time': {'value': scheduled_time, 'errors': [errors.get('scheduled_time')] if errors.get('scheduled_time') else []},
                'judges': {'value': judge_ids, 'errors': [errors.get('judges')] if errors.get('judges') else []},
                'notes': {'value': notes, 'errors': []},
                'match_type': {'value': match_type, 'errors': []},
            }
            return render(request, 'admin/matchmaking/form.html', {
                'form': form_data, 'events': events, 'trainees': trainees, 'judges': judges
            })
        
        # Validate judge assignments for conflicts
        from core.services.matchmaking import MatchmakingService
        service = MatchmakingService()
        
        conflicting_judges = []
        for judge_id in judge_ids:
            if judge_id and not service.validate_judge_assignment(int(judge_id), int(event_id)):
                judge = Judge.objects.get(id=judge_id)
                conflicting_judges.append(judge.profile.user.get_full_name() or judge.profile.user.username)
        
        if conflicting_judges:
            errors['judges'] = f"The following judges are competing in this event and cannot be assigned: {', '.join(conflicting_judges)}"
            events = Event.objects.filter(status__in=['open', 'closed', 'ongoing']).order_by('-event_date')
            trainees = Trainee.objects.filter(status='active').select_related('profile__user')
            judges = Judge.objects.filter(is_active=True).select_related('profile__user')
            
            form_data = {
                'event': {'value': event_id, 'errors': []},
                'competitor1': {'value': competitor1_id, 'errors': []},
                'competitor2': {'value': competitor2_id, 'errors': []},
                'scheduled_time': {'value': scheduled_time, 'errors': []},
                'judges': {'value': judge_ids, 'errors': [errors.get('judges')]},
                'notes': {'value': notes, 'errors': []},
                'match_type': {'value': match_type, 'errors': []},
            }
            return render(request, 'admin/matchmaking/form.html', {
                'form': form_data, 'events': events, 'trainees': trainees, 'judges': judges
            })
        
        # Create match
        match = Match.objects.create(
            event_id=event_id,
            competitor1_id=competitor1_id,
            competitor2_id=competitor2_id,
            scheduled_time=scheduled_time,
            notes=notes,
            match_type=match_type
        )
        
        # Assign judges
        for judge_id in judge_ids:
            if judge_id:
                MatchJudge.objects.create(match=match, judge_id=judge_id)
        
        messages.success(request, 'Match has been created successfully.')
        
        if request.headers.get('HX-Request'):
            response = HttpResponse()
            response['HX-Redirect'] = '/admin/matchmaking/'
            return response
        
        return redirect('admin_matchmaking')
    
    # GET request
    events = Event.objects.filter(status__in=['open', 'closed', 'ongoing']).order_by('-event_date')
    trainees = Trainee.objects.filter(status='active').select_related('profile__user')
    judges = Judge.objects.filter(is_active=True).select_related('profile__user')
    from core.models import Match
    
    return render(request, 'admin/matchmaking/form.html', {
        'form': {}, 'events': events, 'trainees': trainees, 'judges': judges, 
        'match_types': Match.MATCH_TYPE_CHOICES
    })


@admin_required
def match_edit(request, match_id):
    """
    Edit match view.
    Requirements: 5.2
    """
    from core.models import Match, MatchJudge, Event, Trainee, Judge
    
    match = get_object_or_404(Match, id=match_id)
    
    if request.method == 'POST':
        event_id = request.POST.get('event', '').strip()
        competitor1_id = request.POST.get('competitor1', '').strip()
        competitor2_id = request.POST.get('competitor2', '').strip()
        scheduled_time = request.POST.get('scheduled_time', '').strip()
        judge_ids = request.POST.getlist('judges')
        judge_ids = request.POST.getlist('judges')
        notes = request.POST.get('notes', '').strip()
        match_type = request.POST.get('match_type', 'sparring').strip()
        status = request.POST.get('status', 'scheduled').strip()
        
        errors = {}
        if not event_id:
            errors['event'] = 'Event is required'
        if not competitor1_id:
            errors['competitor1'] = 'Competitor 1 is required'
        if not competitor2_id:
            errors['competitor2'] = 'Competitor 2 is required'
        if competitor1_id and competitor2_id and competitor1_id == competitor2_id:
            errors['competitor2'] = 'Competitors must be different'
        if not scheduled_time:
            errors['scheduled_time'] = 'Scheduled time is required'
        if len([j for j in judge_ids if j]) < 3:
            errors['judges'] = 'At least 3 judges must be selected'
        
        if errors:
            events = Event.objects.filter(status__in=['open', 'closed', 'ongoing']).order_by('-event_date')
            trainees = Trainee.objects.filter(status='active').select_related('profile__user')
            judges = Judge.objects.filter(is_active=True).select_related('profile__user')
            
            form_data = {
                'event': {'value': event_id, 'errors': [errors.get('event')] if errors.get('event') else []},
                'competitor1': {'value': competitor1_id, 'errors': [errors.get('competitor1')] if errors.get('competitor1') else []},
                'competitor2': {'value': competitor2_id, 'errors': [errors.get('competitor2')] if errors.get('competitor2') else []},
                'scheduled_time': {'value': scheduled_time, 'errors': [errors.get('scheduled_time')] if errors.get('scheduled_time') else []},
                'judges': {'value': judge_ids, 'errors': [errors.get('judges')] if errors.get('judges') else []},
                'notes': {'value': notes, 'errors': []},
                'status': {'value': status, 'errors': []},
                'match_type': {'value': match_type, 'errors': []},
            }
            return render(request, 'admin/matchmaking/form.html', {
                'form': form_data, 'match': match, 'events': events, 'trainees': trainees, 'judges': judges
            })
        
        # Validate judge assignments for conflicts
        from core.services.matchmaking import MatchmakingService
        service = MatchmakingService()
        
        conflicting_judges = []
        for judge_id in judge_ids:
            if judge_id and not service.validate_judge_assignment(int(judge_id), int(event_id)):
                judge = Judge.objects.get(id=judge_id)
                conflicting_judges.append(judge.profile.user.get_full_name() or judge.profile.user.username)
        
        if conflicting_judges:
            errors['judges'] = f"The following judges are competing in this event and cannot be assigned: {', '.join(conflicting_judges)}"
            events = Event.objects.filter(status__in=['open', 'closed', 'ongoing']).order_by('-event_date')
            trainees = Trainee.objects.filter(status='active').select_related('profile__user')
            judges_list = Judge.objects.filter(is_active=True).select_related('profile__user')
            
            form_data = {
                'event': {'value': event_id, 'errors': []},
                'competitor1': {'value': competitor1_id, 'errors': []},
                'competitor2': {'value': competitor2_id, 'errors': []},
                'scheduled_time': {'value': scheduled_time, 'errors': []},
                'judges': {'value': judge_ids, 'errors': [errors.get('judges')]},
                'notes': {'value': notes, 'errors': []},
                'status': {'value': status, 'errors': []},
                'match_type': {'value': match_type, 'errors': []},
            }
            return render(request, 'admin/matchmaking/form.html', {
                'form': form_data, 'match': match, 'events': events, 'trainees': trainees, 'judges': judges_list
            })
        
        # Update match
        match.event_id = event_id
        match.competitor1_id = competitor1_id
        match.competitor2_id = competitor2_id
        match.scheduled_time = scheduled_time
        match.notes = notes
        match.status = status
        match.match_type = match_type
        match.save()
        
        # Update judges
        match.judge_assignments.all().delete()
        for judge_id in judge_ids:
            if judge_id:
                MatchJudge.objects.create(match=match, judge_id=judge_id)
        
        messages.success(request, 'Match has been updated successfully.')
        
        if request.headers.get('HX-Request'):
            response = HttpResponse()
            response['HX-Redirect'] = '/admin/matchmaking/'
            return response
        
        return redirect('admin_matchmaking')
    
    # GET request
    events = Event.objects.filter(status__in=['open', 'closed', 'ongoing']).order_by('-event_date')
    trainees = Trainee.objects.filter(status='active').select_related('profile__user')
    judges = Judge.objects.filter(is_active=True).select_related('profile__user')
    
    current_judge_ids = list(match.judge_assignments.values_list('judge_id', flat=True))
    
    form_data = {
        'event': {'value': str(match.event_id), 'errors': []},
        'competitor1': {'value': str(match.competitor1_id), 'errors': []},
        'competitor2': {'value': str(match.competitor2_id), 'errors': []},
        'scheduled_time': {'value': match.scheduled_time.strftime('%Y-%m-%dT%H:%M') if match.scheduled_time else '', 'errors': []},
        'judges': {'value': [str(j) for j in current_judge_ids], 'errors': []},
        'notes': {'value': match.notes, 'errors': []},
        'status': {'value': match.status, 'errors': []},
        'match_type': {'value': match.match_type, 'errors': []},
    }
    
    return render(request, 'admin/matchmaking/form.html', {
        'form': form_data, 'match': match, 'events': events, 
        'trainees': trainees, 'judges': judges,
        'match_types': Match.MATCH_TYPE_CHOICES
    })


@admin_required
def match_archive(request, match_id):
    """
    Archive match view.
    Requirements: 5.2
    """
    from core.models import Match, Event
    
    match = get_object_or_404(Match, id=match_id)
    
    if request.method == 'POST':
        match_name = f"{match.competitor1.profile.user.get_full_name()} vs {match.competitor2.profile.user.get_full_name()}"
        match.archived = True
        match.save()
        
        if request.headers.get('HX-Request'):
            from django.middleware.csrf import get_token
            csrf_token = get_token(request)
            # Rebuild the list
            events = Event.objects.prefetch_related(
                'matches__competitor1__profile__user',
                'matches__competitor2__profile__user',
                'matches__judge_assignments__judge__profile__user'
            ).order_by('-event_date')
            
            events_with_matches = []
            for event in events:
                matches = event.matches.filter(archived=False).order_by('scheduled_time')
                if matches.exists():
                    events_with_matches.append({
                        'event': event,
                        'matches': matches
                    })
            
            response = render(request, 'admin/matchmaking/list_partial.html', {'events_with_matches': events_with_matches, 'csrf_token': csrf_token})
            response['HX-Trigger'] = json.dumps({
                'showToast': {'message': f'Match "{match_name}" has been archived.', 'type': 'success'}
            })
            return response
        
        messages.success(request, f'Match "{match_name}" has been archived.')
        return redirect('admin_matchmaking')
    
    return redirect('admin_matchmaking')


@admin_required
def match_delete(request, match_id):
    """
    Delete match view (legacy).
    Requirements: 5.2
    """
    # Redirect to archive instead
    return match_archive(request, match_id)


@admin_required
def archived_matchmaking_list(request):
    """
    Archived matchmaking list view.
    Requirements: 5.1
    """
    from core.models import Match, Event, Judge
    
    # Get all events with archived matches
    events = Event.objects.prefetch_related(
        'matches__competitor1__profile__user',
        'matches__competitor2__profile__user',
        'matches__judge_assignments__judge__profile__user'
    ).order_by('-event_date')
    
    # Apply event filter
    event_filter = request.GET.get('event_filter', '').strip()
    if event_filter:
        events = events.filter(id=event_filter)
    
    # Apply status filter
    status_filter = request.GET.get('status_filter', '').strip()
    
    # Build event data with archived matches
    events_with_matches = []
    for event in events:
        matches = event.matches.filter(archived=True)
        if status_filter:
            matches = matches.filter(status=status_filter)
        matches = matches.order_by('-created_at')
        
        if matches.exists() or not event_filter:
            events_with_matches.append({
                'event': event,
                'matches': matches
            })
    
    # Get all events for filter dropdown
    all_events = Event.objects.all().order_by('-event_date')
    
    context = {
        'events_with_matches': events_with_matches,
        'all_events': all_events,
    }
    
    if request.headers.get('HX-Request'):
        from django.middleware.csrf import get_token
        csrf_token = get_token(request)
        context['csrf_token'] = csrf_token
        return render(request, 'admin/matchmaking/archived_partial.html', context)
    
    return render(request, 'admin/matchmaking/archived.html', context)


@admin_required
def archived_matchmaking_list_partial(request):
    """
    Partial view for HTMX archived matchmaking list updates.
    Requirements: 5.1
    """
    from core.models import Match, Event, Judge
    
    events = Event.objects.prefetch_related(
        'matches__competitor1__profile__user',
        'matches__competitor2__profile__user',
        'matches__judge_assignments__judge__profile__user'
    ).order_by('-event_date')
    
    event_filter = request.GET.get('event_filter', '').strip()
    if event_filter:
        events = events.filter(id=event_filter)
    
    status_filter = request.GET.get('status_filter', '').strip()
    
    events_with_matches = []
    for event in events:
        matches = event.matches.filter(archived=True)
        if status_filter:
            matches = matches.filter(status=status_filter)
        matches = matches.order_by('-created_at')
        
        if matches.exists() or not event_filter:
            events_with_matches.append({
                'event': event,
                'matches': matches
            })
    
    from django.middleware.csrf import get_token
    csrf_token = get_token(request)
    
    return render(request, 'admin/matchmaking/archived_partial.html', {'events_with_matches': events_with_matches, 'csrf_token': csrf_token})


@admin_required
def match_restore(request, match_id):
    """
    Restore archived match view.
    Requirements: 5.2
    """
    from core.models import Match, Event
    
    match = get_object_or_404(Match, id=match_id, archived=True)
    
    if request.method == 'POST':
        match_name = f"{match.competitor1.profile.user.get_full_name()} vs {match.competitor2.profile.user.get_full_name()}"
        match.archived = False
        match.save()
        
        if request.headers.get('HX-Request'):
            from django.middleware.csrf import get_token
            csrf_token = get_token(request)
            # Rebuild the list
            events = Event.objects.prefetch_related(
                'matches__competitor1__profile__user',
                'matches__competitor2__profile__user',
                'matches__judge_assignments__judge__profile__user'
            ).order_by('-event_date')
            
            events_with_matches = []
            for event in events:
                matches = event.matches.filter(archived=True).order_by('scheduled_time')
                if matches.exists():
                    events_with_matches.append({
                        'event': event,
                        'matches': matches
                    })
            
            response = render(request, 'admin/matchmaking/archived_partial.html', {'events_with_matches': events_with_matches, 'csrf_token': csrf_token})
            response['HX-Trigger'] = json.dumps({
                'showToast': {'message': f'Match "{match_name}" has been restored.', 'type': 'success'}
            })
            return response
        
        messages.success(request, f'Match "{match_name}" has been restored.')
        return redirect('admin_archived_matchmaking')
    
    return redirect('admin_archived_matchmaking')


@admin_required
def auto_matchmaking(request):
    """
    Auto-matchmaking view - select event and generate proposed matches.
    Supports regular matches and title matches.
    Requirements: 5.3, 5.4
    """
    from core.models import Event, Judge
    from core.services.matchmaking import MatchmakingService
    
    events = Event.objects.filter(
        status__in=['open', 'closed', 'ongoing']
    ).order_by('-event_date')
    
    judges = Judge.objects.filter(is_active=True).select_related('profile__user')
    proposed_matches = []
    selected_event = None
    
    if request.method == 'POST':
        event_id = request.POST.get('event', '').strip()
        allow_ongoing = request.POST.get('allow_ongoing_matches', 'on') == 'on'
        include_titles = request.POST.get('include_title_matches', 'on') == 'on'
        use_global = request.POST.get('use_global_pool', 'off') == 'on'
        
        if event_id:
            selected_event = Event.objects.get(id=event_id)
            service = MatchmakingService()
            proposed_matches = service.auto_match(
                int(event_id),
                allow_ongoing_matches=allow_ongoing,
                include_title_matches=include_titles,
                use_global_pool=use_global
            )
            
            # Store proposed matches in session for confirmation
            request.session['proposed_matches'] = [
                {
                    'competitor1_id': pm.competitor1.id,
                    'competitor2_id': pm.competitor2.id,
                    'weight_diff': str(pm.weight_diff),
                    'belt_diff': pm.belt_diff,
                    'age_diff': pm.age_diff,
                    'is_title_match': pm.is_title_match,
                }
                for pm in proposed_matches
            ]
            request.session['auto_match_event_id'] = event_id
            request.session['auto_match_options'] = {
                'allow_ongoing_matches': allow_ongoing,
                'include_title_matches': include_titles,
                'use_global_pool': use_global,
            }
    
    context = {
        'events': events,
        'judges': judges,
        'proposed_matches': proposed_matches,
        'selected_event': selected_event,
    }
    
    return render(request, 'admin/matchmaking/auto.html', context)


@admin_required
def auto_matchmaking_confirm(request):
    """
    Confirm and create matches from auto-matchmaking proposals.
    Supports both regular matches and title matches.
    Requirements: 5.4
    """
    from core.models import Match, Event, MatchJudge
    from datetime import datetime, timedelta
    
    if request.method == 'POST':
        event_id = request.session.get('auto_match_event_id')
        proposed_matches = request.session.get('proposed_matches', [])
        judge_ids = request.POST.getlist('judges')
        
        # Validate that at least 3 judges are selected
        valid_judge_ids = [j for j in judge_ids if j]
        if len(valid_judge_ids) < 3:
            messages.error(request, 'At least 3 judges must be selected for auto-matched games.')
            return redirect('admin_auto_matchmaking')
        
        if event_id and proposed_matches:
            event = Event.objects.get(id=event_id)
            
            # Get selected match indices
            selected_indices = request.POST.getlist('selected_matches')
            
            # Base scheduled time (event date at 9:00 AM)
            base_time = datetime.combine(event.event_date, datetime.min.time().replace(hour=9))
            
            created_count = 0
            title_match_count = 0
            for idx in selected_indices:
                try:
                    idx = int(idx)
                    if 0 <= idx < len(proposed_matches):
                        pm = proposed_matches[idx]
                        # Schedule matches 30 minutes apart
                        scheduled_time = base_time + timedelta(minutes=30 * created_count)
                        
                        is_title_match = pm.get('is_title_match', False)
                        notes = "Title Match / Championship" if is_title_match else ""
                        
                        match = Match.objects.create(
                            event_id=event_id,
                            competitor1_id=pm['competitor1_id'],
                            competitor2_id=pm['competitor2_id'],
                            scheduled_time=scheduled_time,
                            notes=notes
                        )
                        
                        # Assign judges to the match
                        for judge_id in valid_judge_ids:
                            MatchJudge.objects.create(match=match, judge_id=judge_id)
                        
                        created_count += 1
                        if is_title_match:
                            title_match_count += 1
                except (ValueError, IndexError):
                    continue
            
            # Clear session data
            if 'proposed_matches' in request.session:
                del request.session['proposed_matches']
            if 'auto_match_event_id' in request.session:
                del request.session['auto_match_event_id']
            if 'auto_match_options' in request.session:
                del request.session['auto_match_options']
            
            match_type_msg = ""
            if title_match_count > 0:
                match_type_msg = f" ({title_match_count} title matches)"
            
            messages.success(request, f'{created_count} matches{match_type_msg} have been created successfully with {len(valid_judge_ids)} judges assigned.')
        
        return redirect('admin_matchmaking')
    
    return redirect('admin_auto_matchmaking')


@admin_required
def payment_list(request):
    """
    Payment list view with status filtering.
    Requirements: 6.1, 6.4
    """
    from core.models import Payment
    
    payments = Payment.objects.select_related('trainee__profile__user').filter(archived=False)
    
    # Apply search filter
    search = request.GET.get('search', '').strip()
    if search:
        payments = payments.filter(
            Q(trainee__profile__user__first_name__icontains=search) |
            Q(trainee__profile__user__last_name__icontains=search) |
            Q(trainee__profile__user__username__icontains=search)
        )
    
    # Apply status filter
    status_filter = request.GET.get('status_filter', '').strip()
    if status_filter:
        payments = payments.filter(status=status_filter)
    
    # Apply type filter
    type_filter = request.GET.get('type_filter', '').strip()
    if type_filter:
        payments = payments.filter(payment_type=type_filter)
    
    # Order by payment date (most recent first)
    payments = payments.order_by('-payment_date')
    
    context = {'payments': payments}
    
    # Return partial for HTMX requests
    if request.headers.get('HX-Request'):
        return render(request, 'admin/payments/list_partial.html', context)
    
    return render(request, 'admin/payments/list.html', context)


@admin_required
def payment_list_partial(request):
    """
    Partial view for HTMX payment list updates.
    Requirements: 6.1, 6.4
    """
    from core.models import Payment
    
    payments = Payment.objects.select_related('trainee__profile__user').filter(archived=False)
    
    # Apply search filter
    search = request.GET.get('search', '').strip()
    if search:
        payments = payments.filter(
            Q(trainee__profile__user__first_name__icontains=search) |
            Q(trainee__profile__user__last_name__icontains=search) |
            Q(trainee__profile__user__username__icontains=search)
        )
    
    # Apply status filter
    status_filter = request.GET.get('status_filter', '').strip()
    if status_filter:
        payments = payments.filter(status=status_filter)
    
    # Apply type filter
    type_filter = request.GET.get('type_filter', '').strip()
    if type_filter:
        payments = payments.filter(payment_type=type_filter)
    
    # Order by payment date
    payments = payments.order_by('-payment_date')
    
    return render(request, 'admin/payments/list_partial.html', {'payments': payments})


@admin_required
def payment_add(request):
    """
    Add new payment view.
    Requirements: 6.2, 6.3
    """
    from core.models import Payment
    
    if request.method == 'POST':
        trainee_id = request.POST.get('trainee', '').strip()
        amount = request.POST.get('amount', '').strip()
        payment_type = request.POST.get('payment_type', '').strip()
        payment_method = request.POST.get('payment_method', '').strip()
        status = request.POST.get('status', 'pending').strip()
        notes = request.POST.get('notes', '').strip()
        
        # Validation
        errors = {}
        if not trainee_id:
            errors['trainee'] = 'Trainee is required'
        if not amount:
            errors['amount'] = 'Amount is required'
        else:
            try:
                amount_decimal = float(amount)
                if amount_decimal <= 0:
                    errors['amount'] = 'Amount must be greater than 0'
            except ValueError:
                errors['amount'] = 'Amount must be a valid number'
        if not payment_type:
            errors['payment_type'] = 'Payment type is required'
        if not payment_method:
            errors['payment_method'] = 'Payment method is required'
        
        if errors:
            trainees = Trainee.objects.filter(status='active').select_related('profile__user')
            form_data = {
                'trainee': {'value': trainee_id, 'errors': [errors.get('trainee')] if errors.get('trainee') else []},
                'amount': {'value': amount, 'errors': [errors.get('amount')] if errors.get('amount') else []},
                'payment_type': {'value': payment_type, 'errors': [errors.get('payment_type')] if errors.get('payment_type') else []},
                'payment_method': {'value': payment_method, 'errors': [errors.get('payment_method')] if errors.get('payment_method') else []},
                'status': {'value': status, 'errors': []},
                'notes': {'value': notes, 'errors': []},
            }
            return render(request, 'admin/payments/form.html', {'form': form_data, 'trainees': trainees})
        
        # Create payment
        payment = Payment.objects.create(
            trainee_id=trainee_id,
            amount=amount,
            payment_type=payment_type,
            payment_method=payment_method,
            status=status,
            notes=notes
        )
        
        # If status is completed, set completed_at
        if status == 'completed':
            payment.mark_completed()
        
        messages.success(request, 'Payment has been recorded successfully.')
        
        if request.headers.get('HX-Request'):
            response = HttpResponse()
            response['HX-Redirect'] = '/admin/payments/'
            return response
        
        return redirect('admin_payments')
    
    # GET request
    trainees = Trainee.objects.filter(status='active').select_related('profile__user')
    return render(request, 'admin/payments/form.html', {'form': {}, 'trainees': trainees})


@admin_required
def payment_edit(request, payment_id):
    """
    Edit payment view.
    Requirements: 6.2, 6.3
    """
    from core.models import Payment
    
    payment = get_object_or_404(Payment.objects.select_related('trainee__profile__user'), id=payment_id)
    
    if request.method == 'POST':
        trainee_id = request.POST.get('trainee', '').strip()
        amount = request.POST.get('amount', '').strip()
        payment_type = request.POST.get('payment_type', '').strip()
        payment_method = request.POST.get('payment_method', '').strip()
        status = request.POST.get('status', 'pending').strip()
        notes = request.POST.get('notes', '').strip()
        
        # Validation
        errors = {}
        if not trainee_id:
            errors['trainee'] = 'Trainee is required'
        if not amount:
            errors['amount'] = 'Amount is required'
        else:
            try:
                amount_decimal = float(amount)
                if amount_decimal <= 0:
                    errors['amount'] = 'Amount must be greater than 0'
            except ValueError:
                errors['amount'] = 'Amount must be a valid number'
        if not payment_type:
            errors['payment_type'] = 'Payment type is required'
        if not payment_method:
            errors['payment_method'] = 'Payment method is required'
        
        if errors:
            trainees = Trainee.objects.filter(status='active').select_related('profile__user')
            form_data = {
                'trainee': {'value': trainee_id, 'errors': [errors.get('trainee')] if errors.get('trainee') else []},
                'amount': {'value': amount, 'errors': [errors.get('amount')] if errors.get('amount') else []},
                'payment_type': {'value': payment_type, 'errors': [errors.get('payment_type')] if errors.get('payment_type') else []},
                'payment_method': {'value': payment_method, 'errors': [errors.get('payment_method')] if errors.get('payment_method') else []},
                'status': {'value': status, 'errors': []},
                'notes': {'value': notes, 'errors': []},
            }
            return render(request, 'admin/payments/form.html', {'form': form_data, 'payment': payment, 'trainees': trainees})
        
        # Update payment
        old_status = payment.status
        payment.trainee_id = trainee_id
        payment.amount = amount
        payment.payment_type = payment_type
        payment.payment_method = payment_method
        payment.status = status
        payment.notes = notes
        
        # If status changed to completed, set completed_at
        if status == 'completed' and old_status != 'completed':
            payment.mark_completed()
        else:
            payment.save()
        
        messages.success(request, 'Payment has been updated successfully.')
        
        if request.headers.get('HX-Request'):
            response = HttpResponse()
            response['HX-Redirect'] = '/admin/payments/'
            return response
        
        return redirect('admin_payments')
    
    # GET request
    trainees = Trainee.objects.filter(status='active').select_related('profile__user')
    form_data = {
        'trainee': {'value': str(payment.trainee_id), 'errors': []},
        'amount': {'value': str(payment.amount), 'errors': []},
        'payment_type': {'value': payment.payment_type, 'errors': []},
        'payment_method': {'value': payment.payment_method, 'errors': []},
        'status': {'value': payment.status, 'errors': []},
        'notes': {'value': payment.notes, 'errors': []},
    }
    return render(request, 'admin/payments/form.html', {'form': form_data, 'payment': payment, 'trainees': trainees})


@admin_required
def payment_delete(request, payment_id):
    """
    Delete payment view.
    Requirements: 6.3
    """
    from core.models import Payment
    
    payment = get_object_or_404(Payment, id=payment_id)
    
    if request.method == 'DELETE' or request.method == 'POST':
        payment.delete()
        
        if request.headers.get('HX-Request'):
            payments = Payment.objects.select_related('trainee__profile__user').order_by('-payment_date')
            response = render(request, 'admin/payments/list_partial.html', {'payments': payments})
            response['HX-Trigger'] = json.dumps({
                'showToast': {'message': 'Payment has been deleted.', 'type': 'success'}
            })
            return response
        
        messages.success(request, 'Payment has been deleted.')
        return redirect('admin_payments')
    
    return redirect('admin_payments')


@admin_required
def payment_mark_completed(request, payment_id):
    """
    Mark payment as completed via HTMX.
    Requirements: 6.5
    """
    from core.models import Payment
    
    payment = get_object_or_404(Payment, id=payment_id)
    
    if request.method == 'POST':
        payment.mark_completed()
        
        if request.headers.get('HX-Request'):
            # Return updated row for HTMX
            response = render(request, 'admin/payments/row_partial.html', {'payment': payment})
            response['HX-Trigger'] = json.dumps({
                'showToast': {'message': 'Payment marked as completed.', 'type': 'success'}
            })
            return response
        
        messages.success(request, 'Payment marked as completed.')
    
    return redirect('admin_payments')


@admin_required
def archived_payments_list(request):
    """
    View archived payments with search and filter options.
    Requirements: 6.1, 6.4
    """
    from core.models import Payment
    
    payments = Payment.objects.select_related('trainee__profile__user').filter(archived=True)
    
    # Apply search filter
    search = request.GET.get('search', '').strip()
    if search:
        payments = payments.filter(
            Q(trainee__profile__user__first_name__icontains=search) |
            Q(trainee__profile__user__last_name__icontains=search) |
            Q(trainee__profile__user__username__icontains=search)
        )
    
    # Apply status filter
    status_filter = request.GET.get('status_filter', '').strip()
    if status_filter:
        payments = payments.filter(status=status_filter)
    
    # Apply type filter
    type_filter = request.GET.get('type_filter', '').strip()
    if type_filter:
        payments = payments.filter(payment_type=type_filter)
    
    # Order by payment date (most recent first)
    payments = payments.order_by('-payment_date')
    
    context = {'payments': payments}
    
    # Return partial for HTMX requests
    if request.headers.get('HX-Request'):
        return render(request, 'admin/payments/archived_list_partial.html', context)
    
    return render(request, 'admin/payments/archived_list.html', context)


@admin_required
def archived_payments_list_partial(request):
    """
    Partial view for HTMX archived payment list updates.
    Requirements: 6.1, 6.4
    """
    from core.models import Payment
    
    payments = Payment.objects.select_related('trainee__profile__user').filter(archived=True)
    
    # Apply search filter
    search = request.GET.get('search', '').strip()
    if search:
        payments = payments.filter(
            Q(trainee__profile__user__first_name__icontains=search) |
            Q(trainee__profile__user__last_name__icontains=search) |
            Q(trainee__profile__user__username__icontains=search)
        )
    
    # Apply status filter
    status_filter = request.GET.get('status_filter', '').strip()
    if status_filter:
        payments = payments.filter(status=status_filter)
    
    # Apply type filter
    type_filter = request.GET.get('type_filter', '').strip()
    if type_filter:
        payments = payments.filter(payment_type=type_filter)
    
    # Order by payment date
    payments = payments.order_by('-payment_date')
    
    return render(request, 'admin/payments/archived_list_partial.html', {'payments': payments})


@admin_required
def payment_archive(request, payment_id):
    """
    Archive a payment (soft delete).
    Requirements: 6.1
    """
    from core.models import Payment
    
    payment = get_object_or_404(Payment, id=payment_id)
    
    if request.method == 'POST':
        payment.archived = True
        payment.save()
        
        if request.headers.get('HX-Request'):
            payments = Payment.objects.select_related('trainee__profile__user').filter(archived=False).order_by('-payment_date')
            response = render(request, 'admin/payments/list_partial.html', {'payments': payments})
            response['HX-Trigger'] = json.dumps({
                'showToast': {'message': 'Payment has been archived.', 'type': 'success'}
            })
            return response
        
        messages.success(request, 'Payment has been archived.')
        return redirect('admin_payments')
    
    return redirect('admin_payments')


@admin_required
def payment_restore(request, payment_id):
    """
    Restore an archived payment.
    Requirements: 6.1
    """
    from core.models import Payment
    
    payment = get_object_or_404(Payment, id=payment_id)
    
    if request.method == 'POST':
        payment.archived = False
        payment.save()
        
        if request.headers.get('HX-Request'):
            payments = Payment.objects.select_related('trainee__profile__user').filter(archived=True).order_by('-payment_date')
            response = render(request, 'admin/payments/archived_list_partial.html', {'payments': payments})
            response['HX-Trigger'] = json.dumps({
                'showToast': {'message': 'Payment has been restored.', 'type': 'success'}
            })
            return response
        
        messages.success(request, 'Payment has been restored.')
        return redirect('admin_archived_payments')
    
    return redirect('admin_archived_payments')


@admin_required
def reports_view(request):
    """
    Reports view with type selection and date range.
    Requirements: 7.1, 7.2
    """
    from core.services.reports import ReportService
    from datetime import date, timedelta
    
    report_service = ReportService()
    report_data = None
    report_type = None
    
    # Get all events for event report dropdown
    events = Event.objects.all().order_by('-event_date')
    
    # Default date range (last 30 days)
    default_end_date = date.today()
    default_start_date = default_end_date - timedelta(days=30)
    
    if request.method == 'POST':
        report_type = request.POST.get('report_type', '').strip()
        start_date_str = request.POST.get('start_date', '').strip()
        end_date_str = request.POST.get('end_date', '').strip()
        event_id = request.POST.get('event_id', '').strip()
        
        # Parse dates
        try:
            start_date = date.fromisoformat(start_date_str) if start_date_str else default_start_date
            end_date = date.fromisoformat(end_date_str) if end_date_str else default_end_date
        except ValueError:
            start_date = default_start_date
            end_date = default_end_date
        
        # Generate report based on type
        if report_type == 'membership':
            report_data = report_service.membership_report(start_date, end_date)
        elif report_type == 'financial':
            report_data = report_service.financial_report(start_date, end_date)
        elif report_type == 'event' and event_id:
            try:
                report_data = report_service.event_report(int(event_id))
            except Event.DoesNotExist:
                report_data = None
    
    context = {
        'report_data': report_data,
        'report_type': report_type,
        'events': events,
        'default_start_date': default_start_date.isoformat(),
        'default_end_date': default_end_date.isoformat(),
    }
    
    return render(request, 'admin/reports/list.html', context)


@admin_required
def reports_export(request):
    """
    Export report as PDF or CSV.
    Requirements: 7.3
    """
    from core.services.reports import ReportService
    from datetime import date, timedelta
    
    report_service = ReportService()
    
    report_type = request.GET.get('report_type', '').strip()
    export_format = request.GET.get('format', 'pdf').strip()
    start_date_str = request.GET.get('start_date', '').strip()
    end_date_str = request.GET.get('end_date', '').strip()
    event_id = request.GET.get('event_id', '').strip()
    
    # Default date range
    default_end_date = date.today()
    default_start_date = default_end_date - timedelta(days=30)
    
    # Parse dates
    try:
        start_date = date.fromisoformat(start_date_str) if start_date_str else default_start_date
        end_date = date.fromisoformat(end_date_str) if end_date_str else default_end_date
    except ValueError:
        start_date = default_start_date
        end_date = default_end_date
    
    # Generate report data
    report_data = None
    if report_type == 'membership':
        report_data = report_service.membership_report(start_date, end_date)
    elif report_type == 'financial':
        report_data = report_service.financial_report(start_date, end_date)
    elif report_type == 'event' and event_id:
        try:
            report_data = report_service.event_report(int(event_id))
        except Event.DoesNotExist:
            return HttpResponse('Event not found', status=404)
    
    if not report_data:
        return HttpResponse('Invalid report type', status=400)
    
    # Export based on format
    if export_format == 'pdf':
        pdf_content = report_service.export_pdf(report_data, report_type)
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{report_type}_report.pdf"'
        return response
    elif export_format == 'csv':
        csv_content = report_service.export_csv(report_data, report_type)
        response = HttpResponse(csv_content, content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{report_type}_report.csv"'
        return response
    
    return HttpResponse('Invalid export format', status=400)


@admin_required
def trainee_export(request):
    """
    Export trainee list as PDF or CSV with optional filters and organization format.
    Supports filtering by specific trainee IDs or using regular filters.
    Requirements: 3.1, 3.6
    """
    from core.services.reports import ReportService
    
    report_service = ReportService()
    
    file_format = request.GET.get('format', 'pdf').strip()  # file format: pdf or csv
    export_org = request.GET.get('export_by', 'user').strip()  # organization: user or belt
    status_filter = request.GET.get('status_filter', '').strip() or None
    belt_filter = request.GET.get('belt_filter', '').strip() or None
    trainee_ids_str = request.GET.get('trainee_ids', '').strip()  # NEW: comma-separated trainee IDs
    
    # Parse trainee_ids if provided
    trainee_ids = None
    if trainee_ids_str:
        try:
            trainee_ids = [int(id.strip()) for id in trainee_ids_str.split(',') if id.strip().isdigit()]
        except (ValueError, AttributeError):
            trainee_ids = None
    
    # Validate export_by parameter
    if export_org not in ['user', 'belt']:
        export_org = 'user'
    
    # Generate trainee report with specified organization
    report_data = report_service.trainee_report(
        status_filter=status_filter, 
        belt_filter=belt_filter,
        trainee_ids=trainee_ids,
        export_format=f'by_{export_org}'
    )
    
    # Export based on file format
    if file_format == 'pdf':
        pdf_content = report_service.export_pdf(report_data, 'trainee_list')
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="trainees_{export_org}.pdf"'
        return response
    elif file_format == 'csv':
        csv_content = report_service.export_csv(report_data, 'trainee_list')
        response = HttpResponse(csv_content, content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="trainees_{export_org}.csv"'
        return response
    
    return HttpResponse('Invalid export format', status=400)


# Belt Rank Promotion Views

@admin_required
def belt_rank_promotion_list(request):
    """
    List all trainees with belt rank promotion management interface.
    Allows admin to view current belt ranks and promote trainees.
    """
    trainees = Trainee.objects.select_related('profile__user', 'points').prefetch_related('belt_rank_progress').all()
    
    # Apply search filter
    search = request.GET.get('search', '').strip()
    if search:
        trainees = trainees.filter(
            Q(profile__user__first_name__icontains=search) |
            Q(profile__user__last_name__icontains=search) |
            Q(profile__user__username__icontains=search) |
            Q(belt_rank__icontains=search)
        )
    
    # Apply belt filter
    belt_filter = request.GET.get('belt_filter', '').strip()
    if belt_filter:
        trainees = trainees.filter(belt_rank=belt_filter)
    
    # Apply status filter
    status_filter = request.GET.get('status_filter', '').strip()
    if status_filter:
        trainees = trainees.filter(status=status_filter)
    
    # Order by name
    trainees = trainees.order_by('profile__user__first_name', 'profile__user__last_name')
    
    # Get all belt rank choices for filter dropdown
    belt_choices = Trainee.BELT_CHOICES
    
    context = {
        'trainees': trainees,
        'belt_choices': belt_choices,
        'search_query': search,
        'belt_filter': belt_filter,
        'status_filter': status_filter,
    }
    
    # Return partial for HTMX requests
    if request.headers.get('HX-Request'):
        return render(request, 'admin/belt_promotion/list_partial.html', context)
    
    return render(request, 'admin/belt_promotion/list.html', context)


@admin_required
def belt_rank_promotion_list_partial(request):
    """
    Partial view for HTMX belt promotion list updates.
    """
    trainees = Trainee.objects.select_related('profile__user', 'points').prefetch_related('belt_rank_progress').all()
    
    # Apply search filter
    search = request.GET.get('search', '').strip()
    if search:
        trainees = trainees.filter(
            Q(profile__user__first_name__icontains=search) |
            Q(profile__user__last_name__icontains=search) |
            Q(profile__user__username__icontains=search) |
            Q(belt_rank__icontains=search)
        )
    
    # Apply belt filter
    belt_filter = request.GET.get('belt_filter', '').strip()
    if belt_filter:
        trainees = trainees.filter(belt_rank=belt_filter)
    
    # Apply status filter
    status_filter = request.GET.get('status_filter', '').strip()
    if status_filter:
        trainees = trainees.filter(status=status_filter)
    
    # Order by name
    trainees = trainees.order_by('profile__user__first_name', 'profile__user__last_name')
    
    # Get belt choices for filter dropdown
    belt_choices = Trainee.BELT_CHOICES
    
    context = {
        'trainees': trainees,
        'belt_choices': belt_choices,
        'search_query': search,
        'belt_filter': belt_filter,
        'status_filter': status_filter,
    }
    
    return render(request, 'admin/belt_promotion/list_partial.html', context)


@admin_required
def belt_rank_promote(request, trainee_id):
    """
    Promote a trainee to the next belt rank with admin override.
    """
    trainee = get_object_or_404(Trainee.objects.select_related('profile__user'), id=trainee_id)
    
    if request.method == 'POST':
        new_belt_rank = request.POST.get('new_belt_rank', '').strip()
        admin_notes = request.POST.get('admin_notes', '').strip()
        
        # Validation
        valid_belts = [belt[0] for belt in Trainee.BELT_CHOICES]
        if new_belt_rank not in valid_belts:
            return render(
                request,
                'admin/belt_promotion/promote_form.html',
                {
                    'trainee': trainee,
                    'belt_choices': Trainee.BELT_CHOICES,
                    'error': 'Invalid belt rank selected'
                }
            )
        
        # Check that new belt is different from current
        if new_belt_rank == trainee.belt_rank:
            return render(
                request,
                'admin/belt_promotion/promote_form.html',
                {
                    'trainee': trainee,
                    'belt_choices': Trainee.BELT_CHOICES,
                    'error': 'New belt rank must be different from current rank'
                }
            )
        
        # Create belt rank progress record
        old_belt_rank = trainee.belt_rank
        try:
            trainee_points = trainee.points.total_points if hasattr(trainee, 'points') else 0
        except:
            trainee_points = 0
        
        # Update trainee belt rank
        trainee.belt_rank = new_belt_rank
        trainee.save()
        
        # Create progress record
        BeltRankProgress.objects.create(
            trainee=trainee,
            old_belt_rank=old_belt_rank,
            new_belt_rank=new_belt_rank,
            points_earned=trainee_points,
            promotion_type='admin_override',
            admin_notes=admin_notes,
            promoted_by=request.user
        )
        
        # Create notification for trainee
        from core.models import Notification
        Notification.objects.create(
            notification_type='belt_promotion',
            title=f'Belt Promotion to {dict(Trainee.BELT_CHOICES).get(new_belt_rank, new_belt_rank)}',
            message=f'Congratulations! Your belt rank has been promoted to {dict(Trainee.BELT_CHOICES).get(new_belt_rank, new_belt_rank)} by admin.',
            recipient=trainee.profile.user,
            trainee=trainee
        )
        
        messages.success(
            request,
            f'{trainee.profile.user.get_full_name() or trainee.profile.user.username} has been promoted to {dict(Trainee.BELT_CHOICES).get(new_belt_rank, new_belt_rank)}.'
        )
        
        # For HTMX requests, redirect with HX-Redirect header
        if request.headers.get('HX-Request'):
            response = HttpResponse()
            response['HX-Redirect'] = '/admin/belt-promotion/'
            return response
        
        return redirect('admin_belt_promotion')
    
    # GET request - show promotion form
    context = {
        'trainee': trainee,
        'belt_choices': Trainee.BELT_CHOICES,
    }
    return render(request, 'admin/belt_promotion/promote_form.html', context)


@admin_required
def belt_rank_promotion_history(request):
    """
    View promotion history for a specific trainee or all trainees.
    """
    # Get all promotion records
    promotions = BeltRankProgress.objects.select_related(
        'trainee__profile__user',
        'promoted_by'
    ).all()
    
    # Apply filter by trainee if specified
    trainee_id = request.GET.get('trainee_id', '').strip()
    if trainee_id:
        promotions = promotions.filter(trainee_id=trainee_id)
    
    # Order by most recent first
    promotions = promotions.order_by('-promoted_at')
    
    context = {
        'promotions': promotions,
        'trainee_id': trainee_id,
    }
    
    # Return partial for HTMX requests
    if request.headers.get('HX-Request'):
        return render(request, 'admin/belt_promotion/history_partial.html', context)
    
    return render(request, 'admin/belt_promotion/history.html', context)


# ============================================================================
# EVALUATION VIEWS
# ============================================================================

@admin_required
def evaluation_list(request):
    """
    List all trainee evaluations with filtering options.
    """
    from core.models import TraineeEvaluation
    
    evaluations = TraineeEvaluation.objects.select_related(
        'trainee__profile__user',
        'evaluator'
    ).filter(archived=False)
    
    # Apply search filter
    search = request.GET.get('search', '').strip()
    if search:
        evaluations = evaluations.filter(
            Q(trainee__profile__user__first_name__icontains=search) |
            Q(trainee__profile__user__last_name__icontains=search) |
            Q(trainee__profile__user__username__icontains=search)
        )
    
    # Apply status filter
    status_filter = request.GET.get('status_filter', '').strip()
    if status_filter:
        evaluations = evaluations.filter(status=status_filter)
    
    # Apply rating filter
    rating_filter = request.GET.get('rating_filter', '').strip()
    if rating_filter:
        evaluations = evaluations.filter(overall_rating=int(rating_filter))
    
    # Order by evaluation date (most recent first)
    evaluations = evaluations.order_by('-evaluated_at')
    
    context = {
        'evaluations': evaluations,
        'search_query': search,
        'status_filter': status_filter,
        'rating_filter': rating_filter,
        'status_choices': [('pending', 'Pending'), ('completed', 'Completed')],
        'rating_choices': [(1, 'Poor'), (2, 'Fair'), (3, 'Good'), (4, 'Very Good'), (5, 'Excellent')],
    }
    
    # Return partial for HTMX requests
    if request.headers.get('HX-Request'):
        return render(request, 'admin/evaluations/list_partial.html', context)
    
    return render(request, 'admin/evaluations/list.html', context)


@admin_required
def evaluation_list_partial(request):
    """
    Partial view for HTMX evaluation list updates.
    """
    from core.models import TraineeEvaluation
    
    evaluations = TraineeEvaluation.objects.select_related(
        'trainee__profile__user',
        'evaluator'
    ).filter(archived=False)
    
    # Apply search filter
    search = request.GET.get('search', '').strip()
    if search:
        evaluations = evaluations.filter(
            Q(trainee__profile__user__first_name__icontains=search) |
            Q(trainee__profile__user__last_name__icontains=search) |
            Q(trainee__profile__user__username__icontains=search)
        )
    
    # Apply status filter
    status_filter = request.GET.get('status_filter', '').strip()
    if status_filter:
        evaluations = evaluations.filter(status=status_filter)
    
    # Apply rating filter
    rating_filter = request.GET.get('rating_filter', '').strip()
    if rating_filter:
        evaluations = evaluations.filter(overall_rating=int(rating_filter))
    
    # Order by evaluation date
    evaluations = evaluations.order_by('-evaluated_at')
    
    return render(request, 'admin/evaluations/list_partial.html', {'evaluations': evaluations})


@admin_required
def evaluation_add(request):
    """
    Create a new trainee evaluation.
    """
    from core.models import TraineeEvaluation
    
    if request.method == 'POST':
        trainee_id = request.POST.get('trainee', '').strip()
        technique = request.POST.get('technique', '1').strip()
        speed = request.POST.get('speed', '1').strip()
        strength = request.POST.get('strength', '1').strip()
        flexibility = request.POST.get('flexibility', '1').strip()
        discipline = request.POST.get('discipline', '1').strip()
        spirit = request.POST.get('spirit', '1').strip()
        overall_rating = request.POST.get('overall_rating', '1').strip()
        comments = request.POST.get('comments', '').strip()
        strengths = request.POST.get('strengths', '').strip()
        areas_for_improvement = request.POST.get('areas_for_improvement', '').strip()
        recommendations = request.POST.get('recommendations', '').strip()
        next_evaluation_date = request.POST.get('next_evaluation_date', '').strip()
        
        # Belt Scoring fields
        attendance_score = request.POST.get('attendance_score', '0').strip()
        sparring_score = request.POST.get('sparring_score', '0').strip()
        achievement_score = request.POST.get('achievement_score', '0').strip()
        performance_score = request.POST.get('performance_score', '0').strip()
        
        # Validation
        errors = {}
        if not trainee_id:
            errors['trainee'] = 'Trainee is required'
        
        if errors:
            trainees = Trainee.objects.filter(status='active').select_related('profile__user').order_by('profile__user__first_name')
            form_data = {
                'trainee': {'value': trainee_id, 'errors': [errors.get('trainee')] if errors.get('trainee') else []},
            }
            return render(request, 'admin/evaluations/form.html', {'form': form_data, 'trainees': trainees, 'rating_choices': TraineeEvaluation.RATING_CHOICES})
        
        # Calculate total belt points: attendance (10%) + sparring (20%) + achievement (10%) + performance (10%)
        try:
            att_score = int(attendance_score)
            spar_score = int(sparring_score)
            ach_score = int(achievement_score)
            perf_score = int(performance_score)
            
            total_belt_points = round((att_score * 0.10) + (spar_score * 0.20) + (ach_score * 0.10) + (perf_score * 0.10))
        except (ValueError, TypeError):
            total_belt_points = 0
        
        # Create evaluation
        evaluation = TraineeEvaluation.objects.create(
            trainee_id=trainee_id,
            evaluator=request.user,
            technique=int(technique),
            speed=int(speed),
            strength=int(strength),
            flexibility=int(flexibility),
            discipline=int(discipline),
            spirit=int(spirit),
            overall_rating=int(overall_rating),
            comments=comments,
            strengths=strengths,
            areas_for_improvement=areas_for_improvement,
            recommendations=recommendations,
            next_evaluation_date=next_evaluation_date if next_evaluation_date else None,
            # Belt Scoring fields
            attendance_score=int(attendance_score),
            sparring_score=int(sparring_score),
            achievement_score=int(achievement_score),
            performance_score=int(performance_score),
            total_belt_points=total_belt_points,
            status='completed'
        )
        
        messages.success(request, f'Evaluation has been created successfully. +{total_belt_points} belt points awarded to {evaluation.trainee.profile.user.get_full_name}.')
        
        if request.headers.get('HX-Request'):
            response = HttpResponse()
            response['HX-Redirect'] = '/admin/evaluations/'
            return response
        
        return redirect('admin_evaluations')
    
    # GET request - show form
    trainees = Trainee.objects.filter(status='active').select_related('profile__user').order_by('profile__user__first_name')
    return render(request, 'admin/evaluations/form.html', {
        'trainees': trainees,
        'rating_choices': TraineeEvaluation.RATING_CHOICES,
        'is_add': True
    })


@admin_required
def evaluation_edit(request, evaluation_id):
    """
    Edit an existing trainee evaluation.
    """
    from core.models import TraineeEvaluation
    
    evaluation = get_object_or_404(TraineeEvaluation.objects.select_related('trainee__profile__user'), id=evaluation_id)
    
    if request.method == 'POST':
         technique = request.POST.get('technique', str(evaluation.technique)).strip()
         speed = request.POST.get('speed', str(evaluation.speed)).strip()
         strength = request.POST.get('strength', str(evaluation.strength)).strip()
         flexibility = request.POST.get('flexibility', str(evaluation.flexibility)).strip()
         discipline = request.POST.get('discipline', str(evaluation.discipline)).strip()
         spirit = request.POST.get('spirit', str(evaluation.spirit)).strip()
         overall_rating = request.POST.get('overall_rating', str(evaluation.overall_rating)).strip()
         comments = request.POST.get('comments', evaluation.comments).strip()
         strengths = request.POST.get('strengths', evaluation.strengths).strip()
         areas_for_improvement = request.POST.get('areas_for_improvement', evaluation.areas_for_improvement).strip()
         recommendations = request.POST.get('recommendations', evaluation.recommendations).strip()
         next_evaluation_date = request.POST.get('next_evaluation_date', '').strip()
         
         # Belt Scoring fields
         attendance_score = request.POST.get('attendance_score', str(evaluation.attendance_score)).strip()
         sparring_score = request.POST.get('sparring_score', str(evaluation.sparring_score)).strip()
         achievement_score = request.POST.get('achievement_score', str(evaluation.achievement_score)).strip()
         performance_score = request.POST.get('performance_score', str(evaluation.performance_score)).strip()
         
         # Calculate total belt points
         try:
             att_score = int(attendance_score)
             spar_score = int(sparring_score)
             ach_score = int(achievement_score)
             perf_score = int(performance_score)
             
             total_belt_points = round((att_score * 0.10) + (spar_score * 0.20) + (ach_score * 0.10) + (perf_score * 0.10))
         except (ValueError, TypeError):
             total_belt_points = evaluation.total_belt_points
         
         # Update evaluation
         evaluation.technique = int(technique)
         evaluation.speed = int(speed)
         evaluation.strength = int(strength)
         evaluation.flexibility = int(flexibility)
         evaluation.discipline = int(discipline)
         evaluation.spirit = int(spirit)
         evaluation.overall_rating = int(overall_rating)
         evaluation.comments = comments
         evaluation.strengths = strengths
         evaluation.areas_for_improvement = areas_for_improvement
         evaluation.recommendations = recommendations
         if next_evaluation_date:
             evaluation.next_evaluation_date = next_evaluation_date
         
         # Update belt scoring fields
         evaluation.attendance_score = int(attendance_score)
         evaluation.sparring_score = int(sparring_score)
         evaluation.achievement_score = int(achievement_score)
         evaluation.performance_score = int(performance_score)
         evaluation.total_belt_points = total_belt_points
         
         evaluation.save()
         
         messages.success(request, f'Evaluation has been updated successfully. Current belt points: +{total_belt_points}.')
         
         if request.headers.get('HX-Request'):
             response = HttpResponse()
             response['HX-Redirect'] = '/admin/evaluations/'
             return response
         
         return redirect('admin_evaluations')
    
    # GET request - show form
    return render(request, 'admin/evaluations/form.html', {
        'evaluation': evaluation,
        'trainees': [evaluation.trainee],
        'rating_choices': TraineeEvaluation.RATING_CHOICES,
        'is_edit': True
    })


@admin_required
def evaluation_delete(request, evaluation_id):
    """
    Delete (archive) an evaluation.
    """
    from core.models import TraineeEvaluation
    
    evaluation = get_object_or_404(TraineeEvaluation, id=evaluation_id)
    
    if request.method == 'POST':
        evaluation.archived = True
        evaluation.save()
        messages.success(request, 'Evaluation has been archived.')
        
        if request.headers.get('HX-Request'):
            response = HttpResponse()
            response['HX-Redirect'] = '/admin/evaluations/'
            return response
        
        return redirect('admin_evaluations')
    
    # GET request - show confirmation
    return render(request, 'admin/evaluations/confirm_delete.html', {'evaluation': evaluation})


@admin_required
def trainee_evaluations(request, trainee_id):
    """
    View all evaluations for a specific trainee.
    """
    from core.models import TraineeEvaluation
    
    trainee = get_object_or_404(Trainee.objects.select_related('profile__user'), id=trainee_id)
    evaluations = TraineeEvaluation.objects.filter(trainee=trainee, archived=False).order_by('-evaluated_at')
    
    context = {
        'trainee': trainee,
        'evaluations': evaluations,
    }
    
    return render(request, 'admin/evaluations/trainee_detail.html', context)


# ============================================================================
# LEADERBOARD VIEWS
# ============================================================================

@admin_required
def leaderboard_view(request):
    """
    Display leaderboard rankings with different timeframe options.
    """
    from core.models import Leaderboard, TraineePoints, Match
    from django.db.models import Count, Q
    
    # Get timeframe filter from request
    timeframe = request.GET.get('timeframe', 'all_time').strip()
    valid_timeframes = ['all_time', 'yearly', 'monthly']
    
    if timeframe not in valid_timeframes:
        timeframe = 'all_time'
    
    # Get leaderboard data
    leaderboards = Leaderboard.objects.filter(
        timeframe=timeframe
    ).select_related(
        'trainee__profile__user',
        'trainee__points'
    ).order_by('rank')[:100]
    
    # Enrich leaderboard data with match counts
    for entry in leaderboards:
        # Get total matches count for this trainee
        total_matches = Match.objects.filter(
            Q(competitor1=entry.trainee) | Q(competitor2=entry.trainee)
        ).count()
        entry.match_count = total_matches
    
    context = {
        'leaderboards': leaderboards,
        'timeframe': timeframe,
        'valid_timeframes': valid_timeframes,
    }
    
    return render(request, 'admin/leaderboard/list.html', context)


# Event PDF Export

@admin_required
def event_export(request):
    """
    Comprehensive event export page with dynamic filtering options.
    """
    events = Event.objects.filter(archived=False).order_by('-event_date')
    
    context = {
        'events': events,
        'total_events': events.count(),
        'open_events': events.filter(status='open').count(),
        'completed_events': events.filter(status='completed').count(),
        'total_participants': sum(e.participant_count for e in events),
        'date_from': '',
        'date_to': '',
    }
    
    if request.method == 'POST':
        action = request.POST.get('action')
        format_type = request.POST.get('format', 'pdf')
        
        # Get filter parameters
        statuses = request.POST.getlist('status')
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        columns = request.POST.getlist('columns')
        include_participants = request.POST.get('include_participants') == 'on'
        include_matches = request.POST.get('include_matches') == 'on'
        include_statistics = request.POST.get('include_statistics') == 'on'
        sort_by = request.POST.get('sort_by', 'date_desc')
        
        # Filter events
        filtered_events = events.filter(status__in=statuses) if statuses else events
        
        if date_from:
            from datetime import datetime
            filtered_events = filtered_events.filter(event_date__gte=date_from)
        
        if date_to:
            from datetime import datetime
            filtered_events = filtered_events.filter(event_date__lte=date_to)
        
        # Sort events
        if sort_by == 'date_asc':
            filtered_events = filtered_events.order_by('event_date')
        elif sort_by == 'name':
            filtered_events = filtered_events.order_by('name')
        elif sort_by == 'participants':
            filtered_events = filtered_events.annotate(
                participant_count=Count('registrations', filter=Q(registrations__status='registered'))
            ).order_by('-participant_count')
        elif sort_by == 'status':
            filtered_events = filtered_events.order_by('status')
        else:  # date_desc
            filtered_events = filtered_events.order_by('-event_date')
        
        # Export based on format
        if format_type == 'pdf':
            return export_events_pdf(
                filtered_events, columns, include_participants,
                include_matches, include_statistics, request
            )
        elif format_type == 'csv':
            return export_events_csv(
                filtered_events, columns, include_participants,
                include_matches, include_statistics, request
            )
        elif format_type == 'excel':
            return export_events_excel(
                filtered_events, columns, include_participants,
                include_matches, include_statistics, request
            )
    
    return render(request, 'admin/events/export.html', context)


def export_events_pdf(events, columns, include_participants, include_matches, include_statistics, request=None):
    """
    Generate comprehensive PDF report.
    """
    from reportlab.lib.pagesizes import A4, letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    from datetime import datetime
    import os
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Events_Report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf"'
    
    doc = SimpleDocTemplate(response, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    story = []
    styles = getSampleStyleSheet()
    
    # Title styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.HexColor('#ff6b35'),
        spaceAfter=6,
        alignment=TA_CENTER,
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,
        spaceAfter=12,
        alignment=TA_CENTER,
    )
    
    section_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#ff6b35'),
        spaceAfter=8,
        spaceBefore=8,
    )
    
    meta_style = ParagraphStyle(
        'MetaStyle',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#6b7280'),
        spaceAfter=2,
        alignment=TA_LEFT,
    )
    
    # Header with logo and metadata
    header_data = []
    
    # Try to add logo if it exists
    logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'media', 'logo.png')
    if os.path.exists(logo_path):
        try:
            logo = Image(logo_path, width=0.5*inch, height=0.5*inch)
            header_table_data = [[logo, Paragraph("<b>BlackCobra Karate Club</b><br/>Event Management Report", 
                                                   ParagraphStyle('HeaderText', parent=styles['Normal'], 
                                                                fontSize=14, textColor=colors.HexColor('#ff6b35'), 
                                                                fontName='Helvetica-Bold'))]]
            header_table = Table(header_table_data, colWidths=[0.8*inch, 5*inch])
            header_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            story.append(header_table)
        except:
            # If logo fails to load, just use text
            story.append(Paragraph("<b>BlackCobra Karate Club</b>", title_style))
            story.append(Paragraph("Event Management Report", styles['Heading3']))
    else:
        # No logo file, use text header
        story.append(Paragraph("<b>BlackCobra Karate Club</b>", title_style))
        story.append(Paragraph("Event Management Report", styles['Heading3']))
    
    story.append(Spacer(1, 0.1 * inch))
    
    # Metadata section - use table for proper layout
    current_user = request.user.get_full_name() or request.user.username if request else 'System'
    
    metadata_data = [
        ['Generated on:', datetime.now().strftime('%B %d, %Y at %H:%M:%S')],
        ['Total Events:', str(events.count())],
    ]
    
    metadata_table = Table(metadata_data, colWidths=[2*inch, 3.8*inch])
    metadata_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('PADDING', (0, 0), (-1, -1), 3),
        ('LINEABOVE', (0, 0), (-1, -1), 0.5, colors.HexColor('#ff6b35')),
        ('LINEBELOW', (0, -1), (-1, -1), 0.5, colors.HexColor('#ff6b35')),
    ]))
    
    story.append(metadata_table)
    story.append(Spacer(1, 0.15 * inch))
    
    # Statistics section
    if include_statistics:
        story.append(Paragraph("Summary Statistics", section_style))
        
        stats_data = [
            ['Total Events', str(events.count())],
            ['Open Events', str(events.filter(status='open').count())],
            ['Completed Events', str(events.filter(status='completed').count())],
            ['Cancelled Events', str(events.filter(status='cancelled').count())],
        ]
        
        stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0f0f0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        
        story.append(stats_table)
        story.append(Spacer(1, 0.2 * inch))
    
    # Events table
    story.append(Paragraph("Event Details", section_style))
    
    # Build column headers based on selection
    headers = []
    col_width_map = {}
    
    if 'name' in columns:
        headers.append('Event Name')
        col_width_map['name'] = 1.2*inch
    if 'date' in columns:
        headers.append('Date')
        col_width_map['date'] = 0.9*inch
    if 'location' in columns:
        headers.append('Location')
        col_width_map['location'] = 1.0*inch
    if 'status' in columns:
        headers.append('Status')
        col_width_map['status'] = 1.1*inch
    if 'participants' in columns:
        headers.append('Participants')
        col_width_map['participants'] = 0.85*inch
    if 'max_participants' in columns:
        headers.append('Max')
        col_width_map['max'] = 0.65*inch
    if 'deadline' in columns:
        headers.append('Deadline')
        col_width_map['deadline'] = 0.9*inch
    if 'description' in columns:
        headers.append('Description')
        col_width_map['description'] = 1.0*inch
    
    # Create column widths list
    col_widths = []
    if 'name' in columns:
        col_widths.append(col_width_map['name'])
    if 'date' in columns:
        col_widths.append(col_width_map['date'])
    if 'location' in columns:
        col_widths.append(col_width_map['location'])
    if 'status' in columns:
        col_widths.append(col_width_map['status'])
    if 'participants' in columns:
        col_widths.append(col_width_map['participants'])
    if 'max_participants' in columns:
        col_widths.append(col_width_map['max'])
    if 'deadline' in columns:
        col_widths.append(col_width_map['deadline'])
    if 'description' in columns:
        col_widths.append(col_width_map['description'])
    
    # Cell style for text wrapping
    cell_style = ParagraphStyle(
        'CellStyle',
        parent=styles['Normal'],
        fontSize=6,
        fontName='Helvetica',
        alignment=TA_CENTER,
        wordWrap='CJK',
        splitLongWords=True,
    )
    
    # Build header row with wrapped text
    header_row = []
    for header in headers:
        header_row.append(Paragraph(f'<b>{header}</b>', cell_style))
    
    events_data = [header_row]
    
    for event in events:
        row = []
        if 'name' in columns:
            text = event.name[:30]
            row.append(Paragraph(text, cell_style))
        if 'date' in columns:
            text = event.event_date.strftime('%Y-%m-%d')
            row.append(Paragraph(text, cell_style))
        if 'location' in columns:
            text = event.location[:20]
            row.append(Paragraph(text, cell_style))
        if 'status' in columns:
            text = event.get_status_display()
            row.append(Paragraph(text, cell_style))
        if 'participants' in columns:
            text = str(event.participant_count)
            row.append(Paragraph(text, cell_style))
        if 'max_participants' in columns:
            text = str(event.max_participants)
            row.append(Paragraph(text, cell_style))
        if 'deadline' in columns:
            text = event.registration_deadline.strftime('%Y-%m-%d') if event.registration_deadline else 'N/A'
            row.append(Paragraph(text, cell_style))
        if 'description' in columns:
            text = (event.description or '')[:25]
            row.append(Paragraph(text, cell_style))
        
        events_data.append(row)
    
    # Create table with optimized column widths
    events_table = Table(events_data, colWidths=col_widths)
    events_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ff6b35')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 7),
        ('FONTSIZE', (0, 1), (-1, -1), 6),
        ('PADDING', (0, 0), (-1, 0), 4),
        ('PADDING', (0, 1), (-1, -1), 3),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
    ]))
    
    story.append(events_table)
    
    # Participants list
    if include_participants:
        story.append(PageBreak())
        story.append(Paragraph("Event Participants", section_style))
        
        for event in events[:5]:  # Limit to first 5 events per page
            registrations = event.registrations.filter(status='registered')
            if registrations.exists():
                story.append(Paragraph(f"<b>{event.name}</b>", styles['Normal']))
                
                participant_data = [['Participant Name', 'Belt Rank', 'Weight Class']]
                for reg in registrations:
                    trainee = reg.trainee
                    participant_data.append([
                        trainee.profile.user.get_full_name(),
                        trainee.get_belt_rank_display(),
                        trainee.weight_class,
                    ])
                
                participant_table = Table(participant_data, colWidths=[2.5*inch, 1.5*inch, 1.8*inch])
                participant_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ff6b35')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('FONTSIZE', (0, 0), (-1, -1), 7),
                    ('PADDING', (0, 0), (-1, -1), 4),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ]))
                
                story.append(participant_table)
                story.append(Spacer(1, 0.1 * inch))
    
    # Signature section at the end
    story.append(PageBreak())
    story.append(Spacer(1, 0.5 * inch))
    
    signature_style = ParagraphStyle(
        'SignatureStyle',
        parent=styles['Normal'],
        fontSize=9,
        fontName='Helvetica',
        alignment=TA_LEFT,
    )
    
    # Signature table layout
    sig_data = [
        ['', ''],
        ['_' * 35, '_' * 35],
        ['Name: ' + current_user, 'Date: ' + datetime.now().strftime('%B %d, %Y')],
        ['', ''],
        ['Prepared by:', ''],
    ]
    
    sig_table = Table(sig_data, colWidths=[2.9*inch, 2.9*inch])
    sig_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(sig_table)
    
    # Build PDF
    doc.build(story)
    return response


def export_events_csv(events, columns, include_participants, include_matches, include_statistics, request=None):
    """
    Generate CSV export.
    """
    import csv
    from datetime import datetime
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="Events_Report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
    
    writer = csv.writer(response)
    
    # Add metadata header
    current_user = request.user.get_full_name() or request.user.username if request else 'System'
    writer.writerow(['BlackCobra Karate Club - Event Report'])
    writer.writerow([f'Generated on: {datetime.now().strftime("%B %d, %Y at %H:%M:%S")}'])
    writer.writerow([f'Prepared by: {current_user}'])
    writer.writerow([])  # Empty row for spacing
    
    # Headers
    headers = []
    if 'name' in columns:
        headers.append('Event Name')
    if 'date' in columns:
        headers.append('Date')
    if 'location' in columns:
        headers.append('Location')
    if 'status' in columns:
        headers.append('Status')
    if 'participants' in columns:
        headers.append('Participants')
    if 'max_participants' in columns:
        headers.append('Max Capacity')
    if 'deadline' in columns:
        headers.append('Registration Deadline')
    if 'description' in columns:
        headers.append('Description')
    
    writer.writerow(headers)
    
    # Data rows
    for event in events:
        row = []
        if 'name' in columns:
            row.append(event.name)
        if 'date' in columns:
            row.append(event.event_date.strftime('%Y-%m-%d'))
        if 'location' in columns:
            row.append(event.location)
        if 'status' in columns:
            row.append(event.get_status_display())
        if 'participants' in columns:
            row.append(event.participant_count)
        if 'max_participants' in columns:
            row.append(event.max_participants)
        if 'deadline' in columns:
            row.append(event.registration_deadline.strftime('%Y-%m-%d'))
        if 'description' in columns:
            row.append(event.description or '')
        
        writer.writerow(row)
    
    return response


def export_events_excel(events, columns, include_participants, include_matches, include_statistics, request=None):
    """
    Generate Excel export (using CSV for now, can be extended with openpyxl).
    """
    # For now, return CSV. Can be upgraded with openpyxl for true Excel format
    return export_events_csv(events, columns, include_participants, include_matches, include_statistics, request)

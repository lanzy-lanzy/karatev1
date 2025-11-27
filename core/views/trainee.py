"""
Trainee views for the BlackCobra Karate Club System.
Handles trainee dashboard, events, matches, and payments.
Requirements: 8.1, 8.2, 9.1-9.4, 10.1-10.3, 11.1-11.3
"""
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from django.utils import timezone

from core.decorators import trainee_required
from core.models import (
    Trainee, Event, EventRegistration, Match, Payment, TraineePoints, BeltRankThreshold, Leaderboard
)
from core.services.leaderboard_service import PointsService, LeaderboardService
from core.forms import TraineeProfileForm, TraineeDetailForm


@trainee_required
def dashboard_view(request):
    """
    Trainee dashboard view displaying profile summary, upcoming events, and scheduled matches.
    Requirements: 8.1, 8.2
    """
    trainee = get_object_or_404(Trainee, profile__user=request.user)
    
    # Get upcoming events the trainee is registered for
    registered_events = Event.objects.filter(
        registrations__trainee=trainee,
        registrations__status='registered',
        event_date__gte=date.today()
    ).order_by('event_date')[:5]
    
    # Get scheduled matches (upcoming)
    upcoming_matches = Match.objects.filter(
        Q(competitor1=trainee) | Q(competitor2=trainee),
        status='scheduled',
        scheduled_time__gte=timezone.now()
    ).select_related('event', 'competitor1', 'competitor2').order_by('scheduled_time')[:5]
    
    # Get total matches count (both scheduled and completed)
    total_matches_count = Match.objects.filter(
        Q(competitor1=trainee) | Q(competitor2=trainee),
        status__in=['scheduled', 'completed']
    ).count()
    
    # Get recent match results
    recent_results = Match.objects.filter(
        Q(competitor1=trainee) | Q(competitor2=trainee),
        status='completed'
    ).select_related('event', 'competitor1', 'competitor2', 'winner').order_by('-scheduled_time')[:3]
    
    # Get pending payments count
    pending_payments_count = Payment.objects.filter(
        trainee=trainee,
        status='pending'
    ).count()
    
    # Get trainee points and belt rank stats
    trainee_points = PointsService.get_trainee_points(trainee)
    next_belt_threshold = PointsService.get_next_belt_threshold(trainee)
    progress_percentage = PointsService.get_progress_percentage(trainee)
    win_rate = PointsService.get_trainee_win_rate(trainee)
    
    # Calculate points needed for next belt
    points_needed = 0
    if trainee_points and next_belt_threshold:
        points_needed = max(0, next_belt_threshold.points_required - trainee_points.total_points)
    
    # Get trainee's leaderboard rank
    leaderboard_entry = LeaderboardService.get_trainee_rank(trainee, 'all_time')
    trainee_rank = leaderboard_entry.rank if leaderboard_entry else None
    
    context = {
        'trainee': trainee,
        'registered_events': registered_events,
        'upcoming_matches': upcoming_matches,
        'total_matches_count': total_matches_count,
        'recent_results': recent_results,
        'pending_payments_count': pending_payments_count,
        # Points and belt rank stats
        'trainee_points': trainee_points,
        'next_belt_threshold': next_belt_threshold,
        'progress_percentage': progress_percentage,
        'win_rate': win_rate,
        'points_needed': points_needed,
        'trainee_rank': trainee_rank,
    }
    
    return render(request, 'trainee/dashboard.html', context)



@trainee_required
def events_view(request):
    """
    Trainee events view displaying open events with registration capability.
    Requirements: 9.1, 9.2, 9.3
    """
    trainee = get_object_or_404(Trainee, profile__user=request.user)
    
    # Get all events that are open or upcoming
    events = Event.objects.filter(
        status__in=['open', 'closed', 'ongoing'],
        event_date__gte=date.today()
    ).order_by('event_date')
    
    # Get trainee's registrations
    registered_event_ids = EventRegistration.objects.filter(
        trainee=trainee,
        status='registered'
    ).values_list('event_id', flat=True)
    
    context = {
        'trainee': trainee,
        'events': events,
        'registered_event_ids': list(registered_event_ids),
    }
    
    response = render(request, 'trainee/events.html', context)
    # Prevent caching so admin changes appear immediately
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


@trainee_required
def event_register(request, event_id):
    """
    Handle event registration for trainee.
    Requirements: 9.2, 9.3, 9.4
    """
    trainee = get_object_or_404(Trainee, profile__user=request.user)
    event = get_object_or_404(Event, id=event_id)
    
    # Check if registration is allowed
    if not event.is_registration_open:
        if date.today() > event.registration_deadline:
            messages.error(request, 'Registration deadline has passed.')
        elif event.is_full:
            messages.error(request, 'Event has reached maximum participants.')
        else:
            messages.error(request, 'Registration is not open for this event.')
        
        if request.headers.get('HX-Request'):
            return HttpResponse(
                '<span class="text-red-600 text-sm">Registration closed</span>',
                status=200
            )
        return redirect('trainee_events')
    
    # Check if already registered
    existing = EventRegistration.objects.filter(
        event=event,
        trainee=trainee,
        status='registered'
    ).exists()
    
    if existing:
        messages.info(request, 'You are already registered for this event.')
        if request.headers.get('HX-Request'):
            return HttpResponse(
                '<span class="inline-flex items-center px-3 py-1.5 rounded-md text-sm font-medium bg-green-100 text-green-800">Registered</span>',
                status=200
            )
        return redirect('trainee_events')
    
    # Create registration
    EventRegistration.objects.create(
        event=event,
        trainee=trainee,
        status='registered'
    )
    
    messages.success(request, f'Successfully registered for {event.name}!')
    
    if request.headers.get('HX-Request'):
        return HttpResponse(
            '<span class="inline-flex items-center px-3 py-1.5 rounded-md text-sm font-medium bg-green-100 text-green-800">Registered</span>',
            status=200
        )
    
    return redirect('trainee_events')


@trainee_required
def event_unregister(request, event_id):
    """
    Handle event unregistration for trainee.
    Requirements: 9.2
    """
    trainee = get_object_or_404(Trainee, profile__user=request.user)
    event = get_object_or_404(Event, id=event_id)
    
    # Check if registration deadline has passed
    if date.today() > event.registration_deadline:
        messages.error(request, 'Cannot unregister after registration deadline.')
        if request.headers.get('HX-Request'):
            return HttpResponse(
                '<span class="inline-flex items-center px-3 py-1.5 rounded-md text-sm font-medium bg-green-100 text-green-800">Registered</span>',
                status=200
            )
        return redirect('trainee_events')
    
    # Find and update registration
    registration = EventRegistration.objects.filter(
        event=event,
        trainee=trainee,
        status='registered'
    ).first()
    
    if registration:
        registration.status = 'withdrawn'
        registration.save()
        messages.success(request, f'Successfully unregistered from {event.name}.')
    
    if request.headers.get('HX-Request'):
        # Return the register button
        return render(request, 'trainee/partials/event_register_button.html', {
            'event': event,
            'is_registered': False,
        })
    
    return redirect('trainee_events')



@trainee_required
def matches_view(request):
    """
    Trainee matches view displaying upcoming and past matches with details.
    Requirements: 10.1, 10.2, 10.3
    """
    trainee = get_object_or_404(Trainee, profile__user=request.user)
    
    # Get upcoming matches
    upcoming_matches = Match.objects.filter(
        Q(competitor1=trainee) | Q(competitor2=trainee),
        status__in=['scheduled', 'ongoing']
    ).select_related(
        'event', 'competitor1', 'competitor2',
        'competitor1__profile__user', 'competitor2__profile__user'
    ).prefetch_related('judge_assignments__judge__profile__user').order_by('scheduled_time')
    
    # Get past matches
    past_matches = Match.objects.filter(
        Q(competitor1=trainee) | Q(competitor2=trainee),
        status='completed'
    ).select_related(
        'event', 'competitor1', 'competitor2', 'winner',
        'competitor1__profile__user', 'competitor2__profile__user'
    ).prefetch_related('judge_assignments__judge__profile__user').order_by('-scheduled_time')
    
    context = {
        'trainee': trainee,
        'upcoming_matches': upcoming_matches,
        'past_matches': past_matches,
    }
    
    return render(request, 'trainee/matches.html', context)



@trainee_required
def payments_view(request):
    """
    Trainee payment history view displaying all payments with pending highlighted.
    Requirements: 11.1, 11.2, 11.3
    """
    trainee = get_object_or_404(Trainee, profile__user=request.user)
    
    # Get pending payments (highlighted at top)
    pending_payments = Payment.objects.filter(
        trainee=trainee,
        status__in=['pending', 'overdue']
    ).order_by('-payment_date')
    
    # Get completed/other payments
    other_payments = Payment.objects.filter(
        trainee=trainee
    ).exclude(
        status__in=['pending', 'overdue']
    ).order_by('-payment_date')
    
    context = {
        'trainee': trainee,
        'pending_payments': pending_payments,
        'other_payments': other_payments,
    }
    
    return render(request, 'trainee/payments.html', context)


@trainee_required
def profile_view(request):
    """
    Trainee profile view - displays current profile information.
    """
    trainee = get_object_or_404(Trainee, profile__user=request.user)
    
    context = {
        'trainee': trainee,
    }
    
    return render(request, 'trainee/profile.html', context)


@trainee_required
def profile_edit(request):
    """
    Trainee profile edit view - allows updating profile and training information.
    Includes profile picture upload.
    """
    trainee = get_object_or_404(Trainee, profile__user=request.user)
    profile = trainee.profile
    
    if request.method == 'POST':
        profile_form = TraineeProfileForm(request.POST, request.FILES, instance=profile)
        detail_form = TraineeDetailForm(request.POST, instance=trainee)
        
        if profile_form.is_valid() and detail_form.is_valid():
            profile_form.save()
            detail_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('trainee_profile')
        else:
            # Combine form errors
            all_errors = profile_form.errors.as_data() if profile_form.errors else {}
            if detail_form.errors:
                all_errors.update(detail_form.errors.as_data())
            
            for field, errors in all_errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        # Pre-populate forms with current data
        initial_data = {
            'first_name': profile.user.first_name,
            'last_name': profile.user.last_name,
            'email': profile.user.email,
        }
        profile_form = TraineeProfileForm(instance=profile, initial=initial_data)
        detail_form = TraineeDetailForm(instance=trainee)
    
    context = {
        'trainee': trainee,
        'profile_form': profile_form,
        'detail_form': detail_form,
    }
    
    return render(request, 'trainee/profile_edit.html', context)

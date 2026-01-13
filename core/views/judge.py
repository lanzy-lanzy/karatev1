"""
Judge views for the BlackCobra Karate Club System.
Handles judge dashboard, events, matches, and results entry.
Requirements: 12.1, 12.2, 12.3, 13.1, 13.2, 13.3, 14.1, 14.2, 14.3, 14.4
"""
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from django.utils import timezone

from core.decorators import judge_required
from core.models import (
    Judge, Event, Match, MatchJudge, MatchResult
)
from core.forms import JudgeProfileForm


@judge_required
def dashboard_view(request):
    """
    Judge dashboard view displaying profile, certification, and upcoming matches count.
    Requirements: 12.1, 12.2
    """
    judge = get_object_or_404(Judge, profile__user=request.user)
    
    # Get count of upcoming assigned matches
    upcoming_matches_count = Match.objects.filter(
        judge_assignments__judge=judge,
        status__in=['scheduled', 'ongoing'],
        scheduled_time__gte=timezone.now()
    ).distinct().count()
    
    # Get recent judging history (completed matches)
    recent_judged_matches = Match.objects.filter(
        judge_assignments__judge=judge,
        status='completed'
    ).select_related(
        'event', 'competitor1__profile__user', 'competitor2__profile__user', 'winner__profile__user'
    ).order_by('-scheduled_time')[:5]
    
    # Get count of matches pending result entry
    pending_results_count = Match.objects.filter(
        judge_assignments__judge=judge,
        status='completed'
    ).exclude(
        result__isnull=False
    ).count()
    
    # Get total matches judged
    total_matches_judged = MatchResult.objects.filter(judge=judge).count()
    
    context = {
        'judge': judge,
        'upcoming_matches_count': upcoming_matches_count,
        'recent_judged_matches': recent_judged_matches,
        'pending_results_count': pending_results_count,
        'total_matches_judged': total_matches_judged,
    }
    
    return render(request, 'judge/dashboard.html', context)



@judge_required
def events_view(request):
    """
    Judge events view displaying events where judge is assigned.
    Requirements: 13.1
    """
    judge = get_object_or_404(Judge, profile__user=request.user)
    
    # Get events where judge is assigned to at least one match
    assigned_event_ids = Match.objects.filter(
        judge_assignments__judge=judge
    ).values_list('event_id', flat=True).distinct()
    
    events = Event.objects.filter(
        id__in=assigned_event_ids,
        event_date__gte=date.today()
    ).order_by('event_date')
    
    # Get past events
    past_events = Event.objects.filter(
        id__in=assigned_event_ids,
        event_date__lt=date.today()
    ).order_by('-event_date')[:5]
    
    context = {
        'judge': judge,
        'events': events,
        'past_events': past_events,
    }
    
    return render(request, 'judge/events.html', context)


@judge_required
def matches_view(request):
    """
    Judge matches view displaying assigned matches with competitor info.
    Requirements: 13.2, 13.3
    """
    judge = get_object_or_404(Judge, profile__user=request.user)
    
    # Get upcoming assigned matches
    upcoming_matches = Match.objects.filter(
        judge_assignments__judge=judge,
        status__in=['scheduled', 'ongoing']
    ).select_related(
        'event', 'competitor1__profile__user', 'competitor2__profile__user'
    ).prefetch_related('judge_assignments__judge__profile__user').order_by('scheduled_time')
    
    # Get past assigned matches
    past_matches = Match.objects.filter(
        judge_assignments__judge=judge,
        status='completed'
    ).select_related(
        'event', 'competitor1__profile__user', 'competitor2__profile__user', 'winner__profile__user'
    ).order_by('-scheduled_time')[:10]
    
    context = {
        'judge': judge,
        'upcoming_matches': upcoming_matches,
        'past_matches': past_matches,
    }
    
    return render(request, 'judge/matches.html', context)


@judge_required
def results_view(request):
    """
    Judge results view displaying matches they have judged with result entry status.
    Requirements: 14.1, 14.2
    """
    judge = get_object_or_404(Judge, profile__user=request.user)
    
    # Get matches pending result entry (scheduled, completed, or ongoing but no result yet)
    pending_results = Match.objects.filter(
        judge_assignments__judge=judge,
        status__in=['scheduled', 'completed', 'ongoing']
    ).exclude(
        result__isnull=False
    ).select_related(
        'event', 'competitor1__profile__user', 'competitor2__profile__user'
    ).order_by('-scheduled_time')
    
    # Get matches with results already submitted
    submitted_results = MatchResult.objects.filter(
        judge=judge
    ).select_related(
        'match__event', 'match__competitor1__profile__user', 
        'match__competitor2__profile__user', 'winner__profile__user'
    ).order_by('-submitted_at')[:10]
    
    context = {
        'judge': judge,
        'pending_results': pending_results,
        'submitted_results': submitted_results,
    }
    
    return render(request, 'judge/results.html', context)


@judge_required
def result_entry(request, match_id):
    """
    Handle result entry for a match.
    Requirements: 14.2, 14.3, 14.4
    """
    judge = get_object_or_404(Judge, profile__user=request.user)
    match = get_object_or_404(Match, id=match_id)
    
    # Verify judge is assigned to this match
    if not MatchJudge.objects.filter(match=match, judge=judge).exists():
        messages.error(request, 'You are not assigned to this match.')
        return redirect('judge_results')
    
    # Check if result already exists (immutability check)
    existing_result = MatchResult.objects.filter(match=match).first()
    if existing_result and existing_result.is_locked:
        messages.error(request, 'Results have already been submitted and locked for this match.')
        return redirect('judge_results')
    
    if request.method == 'POST':
        notes = request.POST.get('notes', '').strip()
        errors = {}
        
        if match.is_promotion_match:
            # Handle promotion scoring
            c1_scores = {}
            c2_scores = {}
            
            try:
                competitor1_score = 0
                competitor2_score = 0
                
                # C1/C2 scores
                for style in ['sparring', 'penan', 'judo', 'breaking']:
                    # Competitor 1
                    val1 = request.POST.get(f'c1_{style}_score', '0').strip()
                    score1 = int(val1)
                    if score1 < 0: 
                        errors['scores'] = 'Scores cannot be negative'
                    c1_scores[f'c1_{style}_score'] = score1
                    competitor1_score += score1
                    
                    # Competitor 2
                    val2 = request.POST.get(f'c2_{style}_score', '0').strip()
                    score2 = int(val2)
                    if score2 < 0:
                        errors['scores'] = 'Scores cannot be negative'
                    c2_scores[f'c2_{style}_score'] = score2
                    competitor2_score += score2
                    
            except ValueError:
                errors['scores'] = 'Invalid score format'
        else:
            competitor1_score = request.POST.get('competitor1_score', '0').strip()
            competitor2_score = request.POST.get('competitor2_score', '0').strip()
            
            # Validation
            try:
                competitor1_score = int(competitor1_score)
                if competitor1_score < 0:
                    errors['competitor1_score'] = 'Score cannot be negative'
            except ValueError:
                errors['competitor1_score'] = 'Invalid score'
            
            try:
                competitor2_score = int(competitor2_score)
                if competitor2_score < 0:
                    errors['competitor2_score'] = 'Score cannot be negative'
            except ValueError:
                errors['competitor2_score'] = 'Invalid score'
        
        # Check if scores are equal
        if not errors and competitor1_score == competitor2_score:
            errors['scores'] = 'Total scores cannot be equal. There must be a clear winner.'
        
        if errors:
            context = {
                'judge': judge,
                'match': match,
                'errors': errors,
                'form_data': {
                    'competitor1_score': competitor1_score if isinstance(competitor1_score, int) else 0,
                    'competitor2_score': competitor2_score if isinstance(competitor2_score, int) else 0,
                    'notes': notes,
                }
            }
            return render(request, 'judge/result_form.html', context)
        
        # Determine winner automatically based on scores
        from core.models import Trainee
        if competitor1_score > competitor2_score:
            winner = match.competitor1
            winner_id = match.competitor1.id
        else:
            winner = match.competitor2
            winner_id = match.competitor2.id
        
        if existing_result:
            # Update existing (only if not locked)
            existing_result.winner = winner
            existing_result.competitor1_score = competitor1_score
            existing_result.competitor2_score = competitor2_score
            existing_result.notes = notes
            existing_result.is_locked = True  # Lock after submission
            
            if match.is_promotion_match:
                for k, v in c1_scores.items():
                    setattr(existing_result, k, v)
                for k, v in c2_scores.items():
                    setattr(existing_result, k, v)
            
            existing_result.save()
        else:
            # Create new result (locked by default)
            MatchResult.objects.create(
                match=match,
                judge=judge,
                winner=winner,
                competitor1_score=competitor1_score,
                competitor2_score=competitor2_score,
                notes=notes,
                is_locked=True,
                **c1_scores if match.is_promotion_match else {},
                **c2_scores if match.is_promotion_match else {}
            )
        
        messages.success(request, 'Match result has been recorded successfully.')
        
        if request.headers.get('HX-Request'):
            response = HttpResponse()
            response['HX-Redirect'] = '/judge/results/'
            return response
        
        return redirect('judge_results')
    
    # GET request - show form
    context = {
        'judge': judge,
        'match': match,
        'errors': {},
        'form_data': {
            'competitor1_score': 0,
            'competitor2_score': 0,
            'notes': '',
        }
    }
    return render(request, 'judge/result_form.html', context)


@judge_required
def profile_edit(request):
    """
    Judge profile edit view - allows updating profile information.
    """
    judge = get_object_or_404(Judge, profile__user=request.user)
    profile = judge.profile
    
    if request.method == 'POST':
        form = JudgeProfileForm(request.POST, request.FILES, instance=profile)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('judge_dashboard')
        else:
            # Display form errors
            for field, errors in form.errors.as_data().items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        # Pre-populate form with current data
        initial_data = {
            'first_name': profile.user.first_name,
            'last_name': profile.user.last_name,
            'email': profile.user.email,
        }
        form = JudgeProfileForm(instance=profile, initial=initial_data)
    
    context = {
        'judge': judge,
        'form': form,
    }
    
    return render(request, 'judge/profile_edit.html', context)

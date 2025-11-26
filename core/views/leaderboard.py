from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import datetime
from core.models import (
    Leaderboard,
    TraineePoints,
    BeltRankProgress,
    BeltRankThreshold,
    Trainee,
)


@login_required
@require_http_methods(["GET"])
def leaderboard_all_time(request):
    """Display all-time leaderboard rankings."""
    leaderboards = Leaderboard.objects.filter(
        timeframe='all_time'
    ).select_related('trainee', 'trainee__profile__user').order_by('rank')
    
    context = {
        'leaderboards': leaderboards,
        'timeframe': 'All Time',
        'timeframe_key': 'all_time',
    }
    return render(request, 'leaderboard/leaderboard.html', context)


@login_required
@require_http_methods(["GET"])
def leaderboard_yearly(request):
    """Display yearly leaderboard rankings."""
    year = request.GET.get('year', datetime.now().year)
    leaderboards = Leaderboard.objects.filter(
        timeframe='yearly',
        year=year
    ).select_related('trainee', 'trainee__profile__user').order_by('rank')
    
    context = {
        'leaderboards': leaderboards,
        'timeframe': f'Year {year}',
        'timeframe_key': 'yearly',
        'year': year,
    }
    return render(request, 'leaderboard/leaderboard.html', context)


@login_required
@require_http_methods(["GET"])
def leaderboard_monthly(request):
    """Display monthly leaderboard rankings."""
    year = request.GET.get('year', datetime.now().year)
    month = request.GET.get('month', datetime.now().month)
    
    leaderboards = Leaderboard.objects.filter(
        timeframe='monthly',
        year=year,
        month=month
    ).select_related('trainee', 'trainee__profile__user').order_by('rank')
    
    month_name = datetime(year, int(month), 1).strftime('%B')
    context = {
        'leaderboards': leaderboards,
        'timeframe': f'{month_name} {year}',
        'timeframe_key': 'monthly',
        'year': year,
        'month': month,
    }
    return render(request, 'leaderboard/leaderboard.html', context)


@login_required
@require_http_methods(["GET"])
def leaderboard_by_belt(request):
    """Display leaderboard rankings filtered by belt rank."""
    belt_rank = request.GET.get('belt', 'white')
    timeframe = request.GET.get('timeframe', 'all_time')
    
    query = Leaderboard.objects.filter(
        belt_rank=belt_rank,
        timeframe=timeframe
    ).select_related('trainee', 'trainee__profile__user').order_by('rank')
    
    belt_display = dict(Trainee.BELT_CHOICES).get(belt_rank, 'Unknown')
    
    context = {
        'leaderboards': query,
        'belt_rank': belt_rank,
        'belt_display': belt_display,
        'timeframe': timeframe,
        'belt_choices': Trainee.BELT_CHOICES,
    }
    return render(request, 'leaderboard/leaderboard_by_belt.html', context)


@login_required
@require_http_methods(["GET"])
def trainee_profile_points(request, trainee_id):
    """Display trainee's points and belt rank progress."""
    trainee = get_object_or_404(Trainee, pk=trainee_id)
    
    try:
        points = TraineePoints.objects.get(trainee=trainee)
    except TraineePoints.DoesNotExist:
        points = None
    
    # Get belt rank progress history
    progress = BeltRankProgress.objects.filter(trainee=trainee).order_by('-promoted_at')
    
    # Get next belt rank threshold
    current_belt_index = [belt[0] for belt in Trainee.BELT_CHOICES].index(trainee.belt_rank)
    next_threshold = None
    if current_belt_index < len(Trainee.BELT_CHOICES) - 1:
        next_belt = Trainee.BELT_CHOICES[current_belt_index + 1][0]
        try:
            next_threshold = BeltRankThreshold.objects.get(belt_rank=next_belt)
        except BeltRankThreshold.DoesNotExist:
            pass
    
    # Calculate progress percentage
    progress_percentage = 0
    if points and next_threshold:
        progress_percentage = min(100, int((points.total_points / next_threshold.points_required) * 100))
    
    context = {
        'trainee': trainee,
        'points': points,
        'progress': progress,
        'next_threshold': next_threshold,
        'progress_percentage': progress_percentage,
    }
    return render(request, 'leaderboard/trainee_profile_points.html', context)


@login_required
@require_http_methods(["GET"])
def belt_rank_progress(request):
    """Display belt rank progression settings and history."""
    thresholds = BeltRankThreshold.objects.all().order_by('points_required')
    
    # Get recent promotions
    recent_promotions = BeltRankProgress.objects.select_related(
        'trainee',
        'trainee__profile__user'
    ).order_by('-promoted_at')[:20]
    
    context = {
        'thresholds': thresholds,
        'recent_promotions': recent_promotions,
    }
    return render(request, 'leaderboard/belt_rank_progress.html', context)

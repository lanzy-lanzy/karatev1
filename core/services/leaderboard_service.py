"""
Leaderboard and Points Service
Handles all leaderboard ranking and point calculation logic.
"""
from datetime import datetime
from django.db.models import Sum
from core.models import (
    TraineePoints,
    Leaderboard,
    BeltRankThreshold,
    Trainee,
    MatchResult,
)


class LeaderboardService:
    """Service for managing leaderboards and rankings."""
    
    @staticmethod
    def update_all_leaderboards():
        """Update all leaderboard rankings (all-time, yearly, monthly)."""
        LeaderboardService.update_leaderboard('all_time')
        LeaderboardService.update_leaderboard('yearly')
        LeaderboardService.update_leaderboard('monthly')
    
    @staticmethod
    def update_leaderboard(timeframe='all_time', year=None, month=None):
        """
        Update leaderboard for a specific timeframe.
        
        Args:
            timeframe: 'all_time', 'yearly', or 'monthly'
            year: Year for yearly/monthly rankings
            month: Month for monthly rankings
        """
        if year is None:
            year = datetime.now().year
        if month is None:
            month = datetime.now().month
        
        # Get all trainees sorted by points
        trainees_points = TraineePoints.objects.all().order_by('-total_points')
        
        for rank, tp in enumerate(trainees_points, 1):
            try:
                Leaderboard.objects.update_or_create(
                    trainee=tp.trainee,
                    timeframe=timeframe,
                    year=year if timeframe in ['yearly', 'monthly'] else None,
                    month=month if timeframe == 'monthly' else None,
                    defaults={
                        'rank': rank,
                        'points': tp.total_points,
                        'belt_rank': tp.trainee.belt_rank,
                    }
                )
            except Exception as e:
                print(f"Error updating leaderboard for {tp.trainee}: {e}")
    
    @staticmethod
    def get_leaderboard(timeframe='all_time', year=None, month=None, belt_rank=None):
        """
        Get leaderboard entries for a specific timeframe.
        
        Args:
            timeframe: 'all_time', 'yearly', or 'monthly'
            year: Year for filtering
            month: Month for filtering
            belt_rank: Optional belt rank filter
        
        Returns:
            QuerySet of Leaderboard entries
        """
        query = Leaderboard.objects.filter(timeframe=timeframe)
        
        if timeframe == 'yearly' and year:
            query = query.filter(year=year)
        elif timeframe == 'monthly' and year and month:
            query = query.filter(year=year, month=month)
        
        if belt_rank:
            query = query.filter(belt_rank=belt_rank)
        
        return query.select_related('trainee', 'trainee__profile__user').order_by('rank')
    
    @staticmethod
    def get_trainee_rank(trainee, timeframe='all_time', year=None, month=None):
        """
        Get a trainee's rank in the leaderboard.
        
        Returns:
            Leaderboard entry or None
        """
        try:
            return Leaderboard.objects.get(
                trainee=trainee,
                timeframe=timeframe,
                year=year if timeframe in ['yearly', 'monthly'] else None,
                month=month if timeframe == 'monthly' else None,
            )
        except Leaderboard.DoesNotExist:
            return None


class PointsService:
    """Service for managing trainee points."""
    
    @staticmethod
    def add_match_result_points(match_result):
        """
        Add points to winner and loser based on match result.
        
        Args:
            match_result: MatchResult instance
        """
        try:
            winner = match_result.winner
            loser = (match_result.match.competitor1 
                    if match_result.match.competitor2 == winner 
                    else match_result.match.competitor2)
            
            # Get or create points records
            winner_points, _ = TraineePoints.objects.get_or_create(trainee=winner)
            loser_points, _ = TraineePoints.objects.get_or_create(trainee=loser)
            
            # Award points
            winner_points.add_win()  # +30 points
            loser_points.add_loss()  # +10 points
            
            # Update leaderboards
            LeaderboardService.update_all_leaderboards()
        except Exception as e:
            print(f"Error adding match result points: {e}")
    
    @staticmethod
    def get_trainee_points(trainee):
        """
        Get or create points record for a trainee.
        
        Returns:
            TraineePoints instance
        """
        points, created = TraineePoints.objects.get_or_create(trainee=trainee)
        return points
    
    @staticmethod
    def get_trainee_win_rate(trainee):
        """
        Calculate trainee's win rate percentage.
        
        Returns:
            Float: win rate as percentage (0-100)
        """
        try:
            points = TraineePoints.objects.get(trainee=trainee)
            total_matches = points.wins + points.losses
            if total_matches == 0:
                return 0
            return (points.wins / total_matches) * 100
        except TraineePoints.DoesNotExist:
            return 0
    
    @staticmethod
    def get_next_belt_threshold(trainee):
        """
        Get the next belt rank threshold for a trainee.
        
        Returns:
            BeltRankThreshold instance or None
        """
        try:
            current_belt_index = [belt[0] for belt in Trainee.BELT_CHOICES].index(
                trainee.belt_rank
            )
            
            if current_belt_index < len(Trainee.BELT_CHOICES) - 1:
                next_belt = Trainee.BELT_CHOICES[current_belt_index + 1][0]
                return BeltRankThreshold.objects.get(belt_rank=next_belt)
        except (ValueError, BeltRankThreshold.DoesNotExist):
            pass
        
        return None
    
    @staticmethod
    def get_progress_percentage(trainee):
        """
        Calculate progress percentage towards next belt rank.
        
        Returns:
            Float: percentage 0-100
        """
        try:
            points = TraineePoints.objects.get(trainee=trainee)
            next_threshold = PointsService.get_next_belt_threshold(trainee)
            
            if next_threshold is None:
                return 100  # Already at black belt
            
            progress = (points.total_points / next_threshold.points_required) * 100
            return min(100, progress)
        except TraineePoints.DoesNotExist:
            return 0

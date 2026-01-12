"""
Matchmaking Service for the BlackCobra Karate Club System.
Handles auto-matchmaking algorithm and match creation.
Requirements: 5.3, 5.4, 5.5, 5.6
"""
from dataclasses import dataclass
from typing import List, Optional
from decimal import Decimal
from datetime import datetime

from core.models import Event, Trainee, Judge, Match, MatchJudge, EventRegistration


@dataclass
class ProposedMatch:
    """Represents a proposed match from auto-matchmaking."""
    competitor1: Trainee
    competitor2: Trainee
    weight_diff: Decimal
    belt_diff: int
    age_diff: int
    score: float  # Lower is better
    is_title_match: bool = False  # Whether this is a title/championship match


# Belt rank order for adjacency calculation
BELT_ORDER = ['white', 'yellow', 'orange', 'green', 'blue', 'brown', 'black']


def get_belt_index(belt_rank: str) -> int:
    """Get the index of a belt rank for comparison."""
    try:
        return BELT_ORDER.index(belt_rank)
    except ValueError:
        return -1


def are_belts_adjacent(belt1: str, belt2: str) -> bool:
    """Check if two belt ranks are the same or adjacent."""
    idx1 = get_belt_index(belt1)
    idx2 = get_belt_index(belt2)
    if idx1 == -1 or idx2 == -1:
        return False
    return abs(idx1 - idx2) <= 1


class MatchmakingService:
    """
    Service for creating matches and auto-matchmaking.
    Requirements: 5.3, 5.4, 5.5, 5.6
    """
    
    # Constraints for auto-matchmaking
    MAX_WEIGHT_DIFF = Decimal('5.0')  # kg
    MAX_AGE_DIFF = 3  # years
    MIN_JUDGES_REQUIRED = 3  # Minimum judges per match
    
    def auto_match(
        self, 
        event_id: int, 
        allow_ongoing_matches: bool = True, 
        include_title_matches: bool = True,
        use_global_pool: bool = False
    ) -> List[ProposedMatch]:
        """
        Generate automatic match pairings for an event or globally.
        
        Rules (Requirements 5.3):
        - Weight class: within 5kg
        - Belt rank: same or adjacent
        - Age group: within 3 years
        
        Args:
            event_id: The event to generate matches for
            allow_ongoing_matches: If True, trainees with ongoing matches can be auto-matched (for title matches)
            include_title_matches: If True, includes title/championship match suggestions
            use_global_pool: If True, match from all active trainees in system (not just event participants)
        
        Returns list of proposed matches for admin review.
        """
        event = Event.objects.get(id=event_id)
        
        # Get trainees - either globally or from event registration
        if use_global_pool:
            # Use all active trainees in the system
            from core.models import Trainee
            all_trainees = list(Trainee.objects.filter(
                status='active',
                archived=False,
                profile__user__is_active=True
            ).select_related('profile__user'))
        else:
            # Get registered trainees for this event only
            registrations = EventRegistration.objects.filter(
                event=event,
                status='registered'
            ).select_related('trainee__profile')
            all_trainees = [reg.trainee for reg in registrations]
        
        # Get trainees with completed matches (candidates for title matches)
        completed_matches = Match.objects.filter(
            event=event,
            status='completed'
        )
        completed_trainee_ids = set()
        for match in completed_matches:
            completed_trainee_ids.add(match.competitor1_id)
            completed_trainee_ids.add(match.competitor2_id)
        
        # Separate trainees into two groups
        if allow_ongoing_matches:
            # All trainees can be matched (for regular matches)
            regular_match_candidates = all_trainees
            
            # Only trainees with completed matches are candidates for title matches
            title_match_candidates = [t for t in all_trainees if t.id in completed_trainee_ids]
        else:
            # Get trainees with ongoing/scheduled matches
            ongoing_matches = Match.objects.filter(event=event).exclude(status__in=['cancelled', 'completed'])
            ongoing_trainee_ids = set()
            for match in ongoing_matches:
                ongoing_trainee_ids.add(match.competitor1_id)
                ongoing_trainee_ids.add(match.competitor2_id)
            
            # Only trainees without ongoing matches can be auto-matched
            regular_match_candidates = [t for t in all_trainees if t.id not in ongoing_trainee_ids]
            title_match_candidates = []
        
        # Generate all valid pairings
        proposed_matches = []
        used_trainees = set()
        
        # Score all possible regular pairings
        all_pairings = []
        for i, t1 in enumerate(regular_match_candidates):
            for t2 in regular_match_candidates[i+1:]:
                if self._is_valid_pairing(t1, t2):
                    score = self._calculate_pairing_score(t1, t2)
                    all_pairings.append((t1, t2, score, False))  # False = not a title match
        
        # Add title match pairings if enabled
        if include_title_matches and title_match_candidates:
            for i, t1 in enumerate(title_match_candidates):
                for t2 in title_match_candidates[i+1:]:
                    if t1.id != t2.id and self._is_valid_pairing(t1, t2):
                        # Title matches get a bonus score (slightly better priority)
                        score = self._calculate_pairing_score(t1, t2) * 0.9  # 10% bonus
                        all_pairings.append((t1, t2, score, True))  # True = is a title match
        
        # Sort by score (lower is better) and greedily select matches
        all_pairings.sort(key=lambda x: x[2])
        
        for t1, t2, score, is_title_match in all_pairings:
            if t1.id not in used_trainees and t2.id not in used_trainees:
                weight_diff = abs(t1.weight - t2.weight)
                belt_diff = abs(get_belt_index(t1.belt_rank) - get_belt_index(t2.belt_rank))
                age_diff = abs((t1.age or 0) - (t2.age or 0))
                
                proposed_matches.append(ProposedMatch(
                    competitor1=t1,
                    competitor2=t2,
                    weight_diff=weight_diff,
                    belt_diff=belt_diff,
                    age_diff=age_diff,
                    score=score,
                    is_title_match=is_title_match
                ))
                
                used_trainees.add(t1.id)
                used_trainees.add(t2.id)
        
        return proposed_matches
    
    def _is_valid_pairing(self, t1: Trainee, t2: Trainee) -> bool:
        """Check if two trainees can be paired based on constraints."""
        # Weight constraint: within 5kg
        weight_diff = abs(t1.weight - t2.weight)
        if weight_diff > self.MAX_WEIGHT_DIFF:
            return False
        
        # Belt rank constraint: same or adjacent
        if not are_belts_adjacent(t1.belt_rank, t2.belt_rank):
            return False
        
        # Age constraint: within 3 years
        age1 = t1.age
        age2 = t2.age
        if age1 is not None and age2 is not None:
            if abs(age1 - age2) > self.MAX_AGE_DIFF:
                return False
        
        return True
    
    def _calculate_pairing_score(self, t1: Trainee, t2: Trainee) -> float:
        """
        Calculate a score for a pairing. Lower is better.
        Prioritizes closer matches in weight, belt, and age.
        """
        weight_diff = float(abs(t1.weight - t2.weight))
        belt_diff = abs(get_belt_index(t1.belt_rank) - get_belt_index(t2.belt_rank))
        
        age1 = t1.age or 0
        age2 = t2.age or 0
        age_diff = abs(age1 - age2)
        
        # Weighted score: weight is most important, then belt, then age
        return (weight_diff * 2) + (belt_diff * 3) + age_diff
    
    def create_match(
        self,
        event_id: int,
        competitor1_id: int,
        competitor2_id: int,
        judge_ids: List[int],
        scheduled_time: datetime,
        is_title_match: bool = False,
        match_notes: str = ""
    ) -> Match:
        """
        Create a manual match assignment.
        Requirements: 5.2
        
        Args:
            event_id: The event for the match
            competitor1_id: First competitor ID
            competitor2_id: Second competitor ID
            judge_ids: List of judge IDs to assign
            scheduled_time: When the match is scheduled
            is_title_match: Whether this is a title/championship match
            match_notes: Optional notes for the match
        """
        notes = "Title Match / Championship" if is_title_match else ""
        if match_notes:
            notes = f"{notes}\n{match_notes}".strip()
        
        match = Match.objects.create(
            event_id=event_id,
            competitor1_id=competitor1_id,
            competitor2_id=competitor2_id,
            scheduled_time=scheduled_time,
            notes=notes
        )
        
        for judge_id in judge_ids:
            MatchJudge.objects.create(match=match, judge_id=judge_id)
        
        return match
    
    def assign_judges(self, match_id: int, judge_ids: List[int]) -> bool:
        """
        Assign judges to a match, validating conflicts.
        Requirements: 5.5, 5.6
        
        Returns True if assignment was successful, False if there was a conflict.
        """
        match = Match.objects.get(id=match_id)
        event = match.event
        
        # Validate minimum number of judges
        if len(judge_ids) < self.MIN_JUDGES_REQUIRED:
            return False
        
        # Validate each judge
        for judge_id in judge_ids:
            if not self.validate_judge_assignment(judge_id, event.id):
                return False
        
        # Clear existing assignments and add new ones
        match.judge_assignments.all().delete()
        for judge_id in judge_ids:
            MatchJudge.objects.create(match=match, judge_id=judge_id)
        
        return True
    
    def validate_judge_assignment(self, judge_id: int, event_id: int) -> bool:
        """
        Validate that a judge is not a competitor in the same event.
        Requirements: 5.5
        
        Returns True if the judge can be assigned, False if there's a conflict.
        """
        judge = Judge.objects.get(id=judge_id)
        
        # Check if the judge's profile has a trainee record
        try:
            trainee = judge.profile.trainee
        except Trainee.DoesNotExist:
            # Judge is not a trainee, no conflict possible
            return True
        
        # Check if the trainee is registered for this event
        is_registered = EventRegistration.objects.filter(
            event_id=event_id,
            trainee=trainee,
            status='registered'
        ).exists()
        
        # Check if the trainee is a competitor in any match in this event
        from django.db.models import Q
        is_competitor = Match.objects.filter(
            event_id=event_id
        ).filter(
            Q(competitor1=trainee) | Q(competitor2=trainee)
        ).exclude(status='cancelled').exists()
        
        return not (is_registered or is_competitor)

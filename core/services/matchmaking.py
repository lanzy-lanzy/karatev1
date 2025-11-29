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
    
    def auto_match(self, event_id: int) -> List[ProposedMatch]:
        """
        Generate automatic match pairings for an event.
        
        Rules (Requirements 5.3):
        - Weight class: within 5kg
        - Belt rank: same or adjacent
        - Age group: within 3 years
        
        Returns list of proposed matches for admin review.
        """
        event = Event.objects.get(id=event_id)
        
        # Get registered trainees for this event
        registrations = EventRegistration.objects.filter(
            event=event,
            status='registered'
        ).select_related('trainee__profile')
        
        trainees = [reg.trainee for reg in registrations]
        
        # Get trainees who already have matches in this event
        existing_matches = Match.objects.filter(event=event).exclude(status='cancelled')
        matched_trainee_ids = set()
        for match in existing_matches:
            matched_trainee_ids.add(match.competitor1_id)
            matched_trainee_ids.add(match.competitor2_id)
        
        # Filter out already matched trainees
        available_trainees = [t for t in trainees if t.id not in matched_trainee_ids]
        
        # Generate all valid pairings
        proposed_matches = []
        used_trainees = set()
        
        # Score all possible pairings
        all_pairings = []
        for i, t1 in enumerate(available_trainees):
            for t2 in available_trainees[i+1:]:
                if self._is_valid_pairing(t1, t2):
                    score = self._calculate_pairing_score(t1, t2)
                    all_pairings.append((t1, t2, score))
        
        # Sort by score (lower is better) and greedily select matches
        all_pairings.sort(key=lambda x: x[2])
        
        for t1, t2, score in all_pairings:
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
                    score=score
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
        scheduled_time: datetime
    ) -> Match:
        """
        Create a manual match assignment.
        Requirements: 5.2
        """
        match = Match.objects.create(
            event_id=event_id,
            competitor1_id=competitor1_id,
            competitor2_id=competitor2_id,
            scheduled_time=scheduled_time
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

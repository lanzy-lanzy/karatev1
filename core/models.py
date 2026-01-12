from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class UserProfile(models.Model):
    """
    Extended user profile with role-based access control.
    Links to Django's built-in User model via OneToOne relationship.
    """
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('trainee', 'Trainee'),
        ('judge', 'Judge'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
    
    def get_dashboard_url(self):
        """Returns the dashboard URL based on user role."""
        dashboard_urls = {
            'admin': '/admin/dashboard/',
            'trainee': '/trainee/dashboard/',
            'judge': '/judge/dashboard/',
        }
        return dashboard_urls.get(self.role, '/')


class Trainee(models.Model):
    """
    Trainee model representing a karate student/member.
    Extends UserProfile with training-specific fields.
    """
    BELT_CHOICES = [
        ('white', 'White'),
        ('green', 'Green'),
        ('brown', 'Brown'),
        ('black', 'Black'),
        ('master_degree', 'Master Degree'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]
    
    # Weight class boundaries in kg
    WEIGHT_CLASS_BOUNDARIES = [
        (Decimal('50'), 'Flyweight'),      # Up to 50kg
        (Decimal('60'), 'Lightweight'),    # 50-60kg
        (Decimal('70'), 'Welterweight'),   # 60-70kg
        (Decimal('80'), 'Middleweight'),   # 70-80kg
        (Decimal('90'), 'Light Heavyweight'),  # 80-90kg
        (Decimal('999'), 'Heavyweight'),   # 90kg+
    ]
    
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='trainee')
    belt_rank = models.CharField(max_length=20, choices=BELT_CHOICES, default='white')
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    weight_class = models.CharField(max_length=20, blank=True)
    emergency_contact = models.CharField(max_length=100)
    emergency_phone = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    archived = models.BooleanField(default=False)
    joined_date = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['profile__user__first_name', 'profile__user__last_name']
        indexes = [
            models.Index(fields=['archived', '-joined_date']),
        ]
    
    def __str__(self):
        return f"{self.profile.user.get_full_name() or self.profile.user.username} - {self.get_belt_rank_display()}"
    
    def calculate_weight_class(self):
        """
        Calculate weight class based on weight.
        Returns the weight class name as a string.
        """
        weight = Decimal(str(self.weight)) if isinstance(self.weight, str) else self.weight
        for boundary, class_name in self.WEIGHT_CLASS_BOUNDARIES:
            if weight <= boundary:
                return class_name
        return 'Heavyweight'
    
    def save(self, *args, **kwargs):
        """Override save to auto-calculate weight class."""
        self.weight_class = self.calculate_weight_class()
        super().save(*args, **kwargs)
    
    @property
    def age(self):
        """Calculate age from profile's date of birth."""
        if self.profile.date_of_birth:
            from datetime import date
            today = date.today()
            dob = self.profile.date_of_birth
            return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return None



class Judge(models.Model):
    """
    Judge model representing a certified official who scores matches.
    Extends UserProfile with certification-specific fields.
    """
    CERTIFICATION_LEVEL_CHOICES = [
        ('regional', 'Regional'),
        ('national', 'National'),
        ('international', 'International'),
    ]
    
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='judge')
    certification_level = models.CharField(max_length=20, choices=CERTIFICATION_LEVEL_CHOICES, default='regional')
    certification_date = models.DateField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Judge {self.profile.user.get_full_name() or self.profile.user.username} - {self.get_certification_level_display()}"


class Event(models.Model):
    """
    Event model representing a karate competition or tournament.
    Requirements: 4.1, 4.2, 4.3, 4.4, 4.5
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('open', 'Open for Registration'),
        ('closed', 'Registration Closed'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    name = models.CharField(max_length=200)
    event_date = models.DateField()
    location = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    registration_deadline = models.DateField()
    max_participants = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-event_date']
        indexes = [
            models.Index(fields=['archived', '-event_date']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.event_date}"
    
    @property
    def participant_count(self):
        """Returns the number of registered participants."""
        return self.registrations.filter(status='registered').count()
    
    @property
    def is_registration_open(self):
        """Check if registration is still open."""
        from datetime import date
        return (
            self.status == 'open' and 
            date.today() <= self.registration_deadline and
            self.participant_count < self.max_participants
        )
    
    @property
    def is_full(self):
        """Check if event has reached max participants."""
        return self.participant_count >= self.max_participants
    
    def should_close(self):
        """
        Check if event should be closed based on:
        1. Registration deadline has passed
        2. Maximum participants reached
        """
        from datetime import date
        
        # Convert registration_deadline to date if it's a string
        deadline = self.registration_deadline
        if isinstance(deadline, str):
            from datetime import datetime
            deadline = datetime.strptime(deadline, '%Y-%m-%d').date()
        
        # Check if registration deadline has passed
        if date.today() > deadline:
            return True, "registration_deadline_passed"
        
        # Check if maximum participants reached
        if self.is_full:
            return True, "max_participants_reached"
        
        return False, None
    
    def close_registration(self):
        """
        Close registration for the event and save the status.
        Returns the reason for closure.
        """
        should_close, reason = self.should_close()
        if should_close and self.status == 'open':
            self.status = 'closed'
            self.save()
            return reason
        return None


class EventRegistration(models.Model):
    """
    EventRegistration model linking trainees to events.
    Requirements: 4.4, 9.1, 9.2, 9.3, 9.4
    """
    STATUS_CHOICES = [
        ('registered', 'Registered'),
        ('cancelled', 'Cancelled'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE, related_name='event_registrations')
    registered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registered')
    
    class Meta:
        unique_together = ['event', 'trainee']
        ordering = ['-registered_at']
    
    def __str__(self):
        return f"{self.trainee} - {self.event.name}"


class Match(models.Model):
    """
    Match model representing a competitive bout between two trainees.
    Requirements: 5.1, 5.2
    """
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    MATCH_TYPE_CHOICES = [
        ('sparring', 'Sparring'),
        ('penan', 'Penan'),
        ('judo', 'Judo'),
        ('breaking', 'Breaking'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='matches')
    competitor1 = models.ForeignKey(
        Trainee, 
        on_delete=models.CASCADE, 
        related_name='matches_as_competitor1'
    )
    competitor2 = models.ForeignKey(
        Trainee, 
        on_delete=models.CASCADE, 
        related_name='matches_as_competitor2'
    )
    winner = models.ForeignKey(
        Trainee, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='won_matches'
    )
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    match_type = models.CharField(max_length=20, choices=MATCH_TYPE_CHOICES, default='sparring')
    notes = models.TextField(blank=True)
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Matches'
        indexes = [
            models.Index(fields=['archived', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.competitor1} vs {self.competitor2} - {self.event.name}"
    
    @property
    def judges(self):
        """Returns all judges assigned to this match."""
        return Judge.objects.filter(match_assignments__match=self)


class MatchJudge(models.Model):
    """
    MatchJudge model for judge assignments to matches.
    Requirements: 5.5, 5.6
    """
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='judge_assignments')
    judge = models.ForeignKey(Judge, on_delete=models.CASCADE, related_name='match_assignments')
    assigned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['match', 'judge']
    
    def __str__(self):
        return f"{self.judge} - {self.match}"


class MatchResult(models.Model):
    """
    MatchResult model for recording match outcomes.
    Requirements: 14.1, 14.2, 14.3, 14.4
    """
    match = models.OneToOneField(Match, on_delete=models.CASCADE, related_name='result')
    judge = models.ForeignKey(Judge, on_delete=models.CASCADE, related_name='submitted_results')
    winner = models.ForeignKey(
        Trainee, 
        on_delete=models.CASCADE, 
        related_name='match_wins'
    )
    competitor1_score = models.IntegerField(default=0)
    competitor2_score = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_locked = models.BooleanField(default=True)  # Results are locked by default after submission
    
    def __str__(self):
        return f"Result: {self.match} - Winner: {self.winner}"
    
    def save(self, *args, **kwargs):
        """Override save to update match winner and status."""
        is_new = not self.pk
        super().save(*args, **kwargs)
        # Update the match with the winner and mark as completed
        self.match.winner = self.winner
        self.match.status = 'completed'
        self.match.save()
        
        # Award points to trainees when result is recorded
        if is_new:
            self._award_match_points()
    
    def _award_match_points(self):
        """Award points to winner and loser based on match result."""
        try:
            # Get or create TraineePoints for both competitors
            winner_points, _ = TraineePoints.objects.get_or_create(trainee=self.winner)
            loser = self.match.competitor1 if self.match.competitor2 == self.winner else self.match.competitor2
            loser_points, _ = TraineePoints.objects.get_or_create(trainee=loser)
            
            # Award points
            winner_points.add_win()
            loser_points.add_loss()
            
            # Update leaderboards
            self._update_leaderboards()
        except Exception as e:
            # Log error but don't fail the save
            print(f"Error awarding points: {e}")
    
    def _update_leaderboards(self):
        """Update leaderboard rankings after points are awarded."""
        from datetime import datetime
        current_year = datetime.now().year
        current_month = datetime.now().month
        
        # Update all-time leaderboard
        self._update_timeframe_leaderboard('all_time', current_year, current_month)
        # Update yearly leaderboard
        self._update_timeframe_leaderboard('yearly', current_year, current_month)
        # Update monthly leaderboard
        self._update_timeframe_leaderboard('monthly', current_year, current_month)
    
    def _update_timeframe_leaderboard(self, timeframe, year, month):
        """Update leaderboard for a specific timeframe."""
        from django.db.models import Sum
        
        if timeframe == 'all_time':
            trainees_points = TraineePoints.objects.all().order_by('-total_points')
            for rank, tp in enumerate(trainees_points, 1):
                Leaderboard.objects.update_or_create(
                    trainee=tp.trainee,
                    timeframe='all_time',
                    year=None,
                    month=None,
                    defaults={
                        'rank': rank,
                        'points': tp.total_points,
                        'belt_rank': tp.trainee.belt_rank,
                    }
                )
        elif timeframe == 'yearly':
            # This would need match dates to filter by year
            # For now, update all trainees' yearly rankings
            trainees_points = TraineePoints.objects.all().order_by('-total_points')
            for rank, tp in enumerate(trainees_points, 1):
                Leaderboard.objects.update_or_create(
                    trainee=tp.trainee,
                    timeframe='yearly',
                    year=year,
                    month=None,
                    defaults={
                        'rank': rank,
                        'points': tp.total_points,
                        'belt_rank': tp.trainee.belt_rank,
                    }
                )
        elif timeframe == 'monthly':
            # This would need match dates to filter by month
            # For now, update all trainees' monthly rankings
            trainees_points = TraineePoints.objects.all().order_by('-total_points')
            for rank, tp in enumerate(trainees_points, 1):
                Leaderboard.objects.update_or_create(
                    trainee=tp.trainee,
                    timeframe='monthly',
                    year=year,
                    month=month,
                    defaults={
                        'rank': rank,
                        'points': tp.total_points,
                        'belt_rank': tp.trainee.belt_rank,
                    }
                )


class Payment(models.Model):
    """
    Payment model for tracking financial transactions.
    Requirements: 6.1, 6.2, 6.3, 6.4, 6.5
    """
    TYPE_CHOICES = [
        ('membership', 'Membership Fee'),
        ('event', 'Event Fee'),
        ('equipment', 'Equipment'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    
    METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Credit/Debit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('check', 'Check'),
        ('other', 'Other'),
    ]
    
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    payment_method = models.CharField(max_length=50, choices=METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    archived = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-payment_date']
        indexes = [
            models.Index(fields=['archived', '-payment_date']),
        ]
    
    def __str__(self):
        return f"{self.trainee} - ${self.amount} ({self.get_payment_type_display()})"
    
    def mark_completed(self):
        """Mark payment as completed and set completion timestamp."""
        from django.utils import timezone
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()


class BeltRankThreshold(models.Model):
    """
    BeltRankThreshold model defining points required for each belt rank.
    """
    BELT_CHOICES = [
        ('white', 'White'),
        ('green', 'Green'),
        ('brown', 'Brown'),
        ('black', 'Black'),
        ('master_degree', 'Master Degree'),
    ]
    
    belt_rank = models.CharField(max_length=20, choices=BELT_CHOICES, unique=True)
    points_required = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['points_required']
    
    def __str__(self):
        return f"{self.get_belt_rank_display()} - {self.points_required} points"


class TraineePoints(models.Model):
    """
    TraineePoints model tracking points earned by trainees through event participation.
    """
    trainee = models.OneToOneField(Trainee, on_delete=models.CASCADE, related_name='points')
    total_points = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    events_participated = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.trainee} - {self.total_points} points"
    
    def add_win(self):
        """Add points for a win (30 points)."""
        self.total_points += 30
        self.wins += 1
        self.save()
        self.check_belt_rank_promotion()
    
    def add_loss(self):
        """Add points for a loss (10 points)."""
        self.total_points += 10
        self.losses += 1
        self.save()
        self.check_belt_rank_promotion()

    def add_points(self, points):
        """Add generic points (e.g. from evaluation)."""
        self.total_points += int(points)
        self.save()
        self.check_belt_rank_promotion()
    
    def check_belt_rank_promotion(self):
        """Check if trainee qualifies for belt rank promotion."""
        # Get next belt rank threshold
        current_belt_index = [belt[0] for belt in Trainee.BELT_CHOICES].index(self.trainee.belt_rank)
        
        if current_belt_index < len(Trainee.BELT_CHOICES) - 1:
            next_belt = Trainee.BELT_CHOICES[current_belt_index + 1][0]
            try:
                threshold = BeltRankThreshold.objects.get(belt_rank=next_belt)
                if self.total_points >= threshold.points_required:
                    # Auto-promote trainee
                    self.trainee.belt_rank = next_belt
                    self.trainee.save()
                    # Create rank progress entry
                    BeltRankProgress.objects.create(
                        trainee=self.trainee,
                        old_belt_rank=Trainee.BELT_CHOICES[current_belt_index][0],
                        new_belt_rank=next_belt,
                        points_earned=self.total_points
                    )
            except BeltRankThreshold.DoesNotExist:
                pass


class BeltRankProgress(models.Model):
    """
    BeltRankProgress model tracking belt rank promotions/changes for trainees.
    """
    PROMOTION_TYPE_CHOICES = [
        ('automatic', 'Automatic'),
        ('admin_override', 'Admin Override'),
    ]
    
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE, related_name='belt_rank_progress')
    old_belt_rank = models.CharField(max_length=20, choices=Trainee.BELT_CHOICES)
    new_belt_rank = models.CharField(max_length=20, choices=Trainee.BELT_CHOICES)
    points_earned = models.IntegerField()
    promotion_type = models.CharField(max_length=20, choices=PROMOTION_TYPE_CHOICES, default='automatic')
    admin_notes = models.TextField(blank=True)
    promoted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='belt_promotions_given')
    promoted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-promoted_at']
    
    def __str__(self):
        return f"{self.trainee} promoted from {self.get_old_belt_rank_display()} to {self.get_new_belt_rank_display()}"


class Leaderboard(models.Model):
    """
    Leaderboard model for tracking trainee rankings by points.
    """
    TIMEFRAME_CHOICES = [
        ('all_time', 'All Time'),
        ('yearly', 'Yearly'),
        ('monthly', 'Monthly'),
    ]
    
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE, related_name='leaderboard_entries')
    rank = models.IntegerField()
    points = models.IntegerField()
    timeframe = models.CharField(max_length=20, choices=TIMEFRAME_CHOICES, default='all_time')
    belt_rank = models.CharField(max_length=20, choices=Trainee.BELT_CHOICES)
    year = models.IntegerField(null=True, blank=True)
    month = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['trainee', 'timeframe', 'year', 'month']
        ordering = ['rank']
    
    def __str__(self):
        return f"#{self.rank} - {self.trainee} ({self.get_timeframe_display()})"


class Notification(models.Model):
    """
    Notification model for in-app notifications.
    Tracks notifications sent to trainees and other users.
    """
    NOTIFICATION_TYPES = [
        ('event_created', 'Event Created'),
        ('event_updated', 'Event Updated'),
        ('belt_promotion', 'Belt Promotion'),
        ('match_scheduled', 'Match Scheduled'),
        ('match_result', 'Match Result'),
        ('event_reminder', 'Event Reminder'),
        ('general', 'General'),
    ]
    
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES, default='general')
    title = models.CharField(max_length=200)
    message = models.TextField()
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    
    # Optional foreign keys for linking to related objects
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications')
    trainee = models.ForeignKey(Trainee, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications')
    
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', '-created_at']),
            models.Index(fields=['recipient', 'is_read']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.recipient.username}"
    
    def mark_as_read(self):
        """Mark notification as read."""
        if not self.is_read:
            from django.utils import timezone
            self.is_read = True
            self.read_at = timezone.now()
            self.save()


class Registration(models.Model):
    """
    Registration model for new member sign-ups requiring admin approval.
    Users must upload medical certificate and waiver documents.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
    ]
    
    # User information
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='registration')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Additional info
    date_of_birth = models.DateField()
    belt_level = models.CharField(max_length=20, choices=Trainee.BELT_CHOICES, default='white')
    
    # Documents
    medical_certificate = models.FileField(upload_to='registrations/medical_certs/')
    waiver = models.FileField(upload_to='registrations/waivers/')
    
    # Status and payment
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid')
    membership_fee = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
    
    # Emergency Contact
    emergency_contact = models.CharField(max_length=100, default='')
    emergency_phone = models.CharField(max_length=20, default='')
    address = models.TextField(blank=True, default='')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='registrations_reviewed')
    rejection_reason = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_status_display()}"


class TraineeEvaluation(models.Model):
    """
    TraineeEvaluation model for assessing trainee performance and progress.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    ]
    
    RATING_CHOICES = [
        (1, 'Poor'),
        (2, 'Fair'),
        (3, 'Good'),
        (4, 'Very Good'),
        (5, 'Excellent'),
    ]
    
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE, related_name='evaluations')
    evaluator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='evaluations_given')
    
    # Evaluation criteria
    technique = models.IntegerField(choices=RATING_CHOICES, default=3, help_text='Overall technique proficiency')
    speed = models.IntegerField(choices=RATING_CHOICES, default=3, help_text='Speed and reaction time')
    strength = models.IntegerField(choices=RATING_CHOICES, default=3, help_text='Physical strength')
    flexibility = models.IntegerField(choices=RATING_CHOICES, default=3, help_text='Flexibility and range of motion')
    discipline = models.IntegerField(choices=RATING_CHOICES, default=3, help_text='Discipline and focus')
    spirit = models.IntegerField(choices=RATING_CHOICES, default=3, help_text='Fighting spirit and determination')
    
    # Overall assessment
    overall_rating = models.IntegerField(choices=RATING_CHOICES, default=3, help_text='Overall performance rating')
    comments = models.TextField(blank=True, help_text='Detailed comments and feedback')
    strengths = models.TextField(blank=True, help_text='Key strengths to build upon')
    areas_for_improvement = models.TextField(blank=True, help_text='Areas that need improvement')
    recommendations = models.TextField(blank=True, help_text='Recommendations for training and development')
    
    # Belt Promotion Scoring (0-100 score for each)
    attendance_score = models.IntegerField(default=0, help_text='Score 0-100. Contributes 10% to points.')
    sparring_score = models.IntegerField(default=0, help_text='Score 0-100. Contributes 20% to points.')
    achievement_score = models.IntegerField(default=0, help_text='Score 0-100. Contributes 10% to points.')
    performance_score = models.IntegerField(default=0, help_text='Score 0-100. Contributes 10% to points.')
    
    total_belt_points = models.IntegerField(default=0, editable=False, help_text='Calculated points added to trainee total')
    is_points_applied = models.BooleanField(default=False, editable=False)
    
    # Status and timestamps
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    evaluated_at = models.DateTimeField(auto_now_add=True)
    next_evaluation_date = models.DateField(null=True, blank=True, help_text='Recommended date for next evaluation')
    archived = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-evaluated_at']
        indexes = [
            models.Index(fields=['trainee', '-evaluated_at']),
            models.Index(fields=['archived', '-evaluated_at']),
        ]
    
    def __str__(self):
        return f"Evaluation: {self.trainee} - {self.evaluated_at.strftime('%Y-%m-%d')}"
    
    @property
    def average_rating(self):
        """Calculate average rating from all criteria."""
        ratings = [
            self.technique,
            self.speed,
            self.strength,
            self.flexibility,
            self.discipline,
            self.spirit,
        ]
        return sum(ratings) / len(ratings) if ratings else 0

    def calculate_belt_points(self):
        """
        Calculate points for belt rank based on weighted scores:
        - Attendance: 10%
        - Sparring: 20%
        - Achievement: 10%
        - Performance: 10% (Overall performance)
        Total possible contribution: 50% of sum?
        User request: "10% for attendance, sparring 20% achievement 10%, overall performance 10%"
        Interpreted as: Point Value = (Attendance * 0.1) + (Sparring * 0.2) + (Achievement * 0.1) + (Performance * 0.1)
        Example: 100 in all gives 10 + 20 + 10 + 10 = 50 points.
        """
        points = (
            (self.attendance_score * 0.10) +
            (self.sparring_score * 0.20) +
            (self.achievement_score * 0.10) +
            (self.performance_score * 0.10)
        )
        return int(points)

    def save(self, *args, **kwargs):
        self.total_belt_points = self.calculate_belt_points()
        
        # If completing the evaluation, apply points
        if self.status == 'completed' and not self.is_points_applied:
            # We need to save self first to get an ID if it's new, but actually we can just apply to trainee
            # However, safer to apply after super().save() ensuring transaction is likely good
            pass
            
        super().save(*args, **kwargs)
        
        if self.status == 'completed' and not self.is_points_applied:
            try:
                trainee_points = self.trainee.points
                trainee_points.add_points(self.total_belt_points)
                self.is_points_applied = True
                # convert to update to avoid recursion loop if save calls signals, though save() here calls super save again
                TraineeEvaluation.objects.filter(pk=self.pk).update(is_points_applied=True)
            except TraineePoints.DoesNotExist:
                pass # Should exist but handle gracefully

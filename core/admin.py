from django.contrib import admin
from core.models import (
    UserProfile,
    Trainee,
    Judge,
    Event,
    EventRegistration,
    Match,
    MatchJudge,
    MatchResult,
    Payment,
    BeltRankThreshold,
    TraineePoints,
    BeltRankProgress,
    Leaderboard,
    Notification,
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email')


@admin.register(Trainee)
class TraineeAdmin(admin.ModelAdmin):
    list_display = ('profile', 'belt_rank', 'weight_class', 'status', 'joined_date')
    list_filter = ('belt_rank', 'status', 'weight_class')
    search_fields = ('profile__user__username', 'profile__user__email')


@admin.register(Judge)
class JudgeAdmin(admin.ModelAdmin):
    list_display = ('profile', 'certification_level', 'is_active')
    list_filter = ('certification_level', 'is_active')
    search_fields = ('profile__user__username',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_date', 'status', 'participant_count', 'max_participants')
    list_filter = ('status', 'event_date')
    search_fields = ('name', 'location')


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('trainee', 'event', 'status', 'registered_at')
    list_filter = ('status', 'registered_at')
    search_fields = ('trainee__profile__user__username', 'event__name')


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('competitor1', 'competitor2', 'event', 'winner', 'status', 'scheduled_time')
    list_filter = ('status', 'scheduled_time')
    search_fields = ('competitor1__profile__user__username', 'competitor2__profile__user__username')


@admin.register(MatchJudge)
class MatchJudgeAdmin(admin.ModelAdmin):
    list_display = ('judge', 'match', 'assigned_at')
    search_fields = ('judge__profile__user__username',)


@admin.register(MatchResult)
class MatchResultAdmin(admin.ModelAdmin):
    list_display = ('match', 'judge', 'winner', 'competitor1_score', 'competitor2_score', 'submitted_at')
    list_filter = ('submitted_at',)
    search_fields = ('match__competitor1__profile__user__username',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('trainee', 'amount', 'payment_type', 'status', 'payment_date')
    list_filter = ('status', 'payment_type', 'payment_date')
    search_fields = ('trainee__profile__user__username',)


@admin.register(BeltRankThreshold)
class BeltRankThresholdAdmin(admin.ModelAdmin):
    list_display = ('belt_rank', 'points_required')
    ordering = ('points_required',)


@admin.register(TraineePoints)
class TraineePointsAdmin(admin.ModelAdmin):
    list_display = ('trainee', 'total_points', 'wins', 'losses', 'events_participated', 'updated_at')
    list_filter = ('updated_at',)
    search_fields = ('trainee__profile__user__username',)
    readonly_fields = ('updated_at',)


@admin.register(BeltRankProgress)
class BeltRankProgressAdmin(admin.ModelAdmin):
    list_display = ('trainee', 'old_belt_rank', 'new_belt_rank', 'points_earned', 'promoted_at')
    list_filter = ('promoted_at', 'new_belt_rank')
    search_fields = ('trainee__profile__user__username',)
    readonly_fields = ('promoted_at',)


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('rank', 'trainee', 'points', 'belt_rank', 'timeframe', 'year', 'month', 'updated_at')
    list_filter = ('timeframe', 'belt_rank', 'year', 'month')
    search_fields = ('trainee__profile__user__username',)
    readonly_fields = ('updated_at',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'notification_type', 'recipient', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('title', 'recipient__username', 'message')
    readonly_fields = ('created_at', 'read_at')
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        """Admin action to mark notifications as read."""
        from django.utils import timezone
        updated = queryset.update(is_read=True, read_at=timezone.now())
        self.message_user(request, f'{updated} notification(s) marked as read.')
    mark_as_read.short_description = "Mark selected notifications as read"
    
    def mark_as_unread(self, request, queryset):
        """Admin action to mark notifications as unread."""
        updated = queryset.update(is_read=False, read_at=None)
        self.message_user(request, f'{updated} notification(s) marked as unread.')
    mark_as_unread.short_description = "Mark selected notifications as unread"

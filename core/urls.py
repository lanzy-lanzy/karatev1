from django.urls import path
from . import views
from .views import admin as admin_views
from .views import trainee as trainee_views
from .views import judge as judge_views
from .views import leaderboard as leaderboard_views
from .views import notifications as notification_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Admin URLs
    path('admin/dashboard/', admin_views.dashboard_view, name='admin_dashboard'),
    
    # Trainee Management URLs (Requirements: 3.1-3.6)
    path('admin/trainees/', admin_views.trainee_list, name='admin_trainees'),
    path('admin/trainees/partial/', admin_views.trainee_list_partial, name='admin_trainee_list_partial'),
    path('admin/trainees/add/', admin_views.trainee_add, name='admin_trainee_add'),
    path('admin/trainees/<int:trainee_id>/edit/', admin_views.trainee_edit, name='admin_trainee_edit'),
    path('admin/trainees/<int:trainee_id>/delete/', admin_views.trainee_delete, name='admin_trainee_delete'),
    
    # Event Management URLs (Requirements: 4.1-4.5)
    path('admin/events/', admin_views.event_list, name='admin_events'),
    path('admin/events/partial/', admin_views.event_list_partial, name='admin_event_list_partial'),
    path('admin/events/add/', admin_views.event_add, name='admin_event_add'),
    path('admin/events/<int:event_id>/', admin_views.event_detail, name='admin_event_detail'),
    path('admin/events/<int:event_id>/edit/', admin_views.event_edit, name='admin_event_edit'),
    path('admin/events/<int:event_id>/delete/', admin_views.event_delete, name='admin_event_delete'),
    path('admin/events/<int:event_id>/status/', admin_views.event_status_update, name='admin_event_status_update'),
    
    # Matchmaking Management URLs (Requirements: 5.1-5.6)
    path('admin/matchmaking/', admin_views.matchmaking_list, name='admin_matchmaking'),
    path('admin/matchmaking/partial/', admin_views.matchmaking_list_partial, name='admin_matchmaking_list_partial'),
    path('admin/matchmaking/add/', admin_views.match_add, name='admin_match_add'),
    path('admin/matchmaking/<int:match_id>/edit/', admin_views.match_edit, name='admin_match_edit'),
    path('admin/matchmaking/<int:match_id>/delete/', admin_views.match_delete, name='admin_match_delete'),
    path('admin/matchmaking/auto/', admin_views.auto_matchmaking, name='admin_auto_matchmaking'),
    path('admin/matchmaking/auto/confirm/', admin_views.auto_matchmaking_confirm, name='admin_auto_matchmaking_confirm'),
    
    # Payment Management URLs (Requirements: 6.1-6.5)
    path('admin/payments/', admin_views.payment_list, name='admin_payments'),
    path('admin/payments/partial/', admin_views.payment_list_partial, name='admin_payment_list_partial'),
    path('admin/payments/add/', admin_views.payment_add, name='admin_payment_add'),
    path('admin/payments/<int:payment_id>/edit/', admin_views.payment_edit, name='admin_payment_edit'),
    path('admin/payments/<int:payment_id>/delete/', admin_views.payment_delete, name='admin_payment_delete'),
    path('admin/payments/<int:payment_id>/complete/', admin_views.payment_mark_completed, name='admin_payment_complete'),
    
    # Reports URLs (Requirements: 7.1-7.4)
    path('admin/reports/', admin_views.reports_view, name='admin_reports'),
    path('admin/reports/export/', admin_views.reports_export, name='admin_reports_export'),
    
    # Trainee URLs (Requirements: 8.1-8.3, 9.1-9.4, 10.1-10.3, 11.1-11.3)
    path('trainee/dashboard/', trainee_views.dashboard_view, name='trainee_dashboard'),
    path('trainee/profile/', trainee_views.profile_view, name='trainee_profile'),
    path('trainee/profile/edit/', trainee_views.profile_edit, name='trainee_profile_edit'),
    path('trainee/events/', trainee_views.events_view, name='trainee_events'),
    path('trainee/events/<int:event_id>/register/', trainee_views.event_register, name='trainee_event_register'),
    path('trainee/events/<int:event_id>/unregister/', trainee_views.event_unregister, name='trainee_event_unregister'),
    path('trainee/matches/', trainee_views.matches_view, name='trainee_matches'),
    path('trainee/payments/', trainee_views.payments_view, name='trainee_payments'),
    
    # Judge URLs (Requirements: 12.1-12.3, 13.1-13.3, 14.1-14.4)
    path('judge/dashboard/', judge_views.dashboard_view, name='judge_dashboard'),
    path('judge/events/', judge_views.events_view, name='judge_events'),
    path('judge/matches/', judge_views.matches_view, name='judge_matches'),
    path('judge/results/', judge_views.results_view, name='judge_results'),
    path('judge/results/<int:match_id>/', judge_views.result_entry, name='judge_result_entry'),
    
    # Leaderboard and Belt Rank URLs
    path('leaderboard/all-time/', leaderboard_views.leaderboard_all_time, name='leaderboard_all_time'),
    path('leaderboard/yearly/', leaderboard_views.leaderboard_yearly, name='leaderboard_yearly'),
    path('leaderboard/monthly/', leaderboard_views.leaderboard_monthly, name='leaderboard_monthly'),
    path('leaderboard/by-belt/', leaderboard_views.leaderboard_by_belt, name='leaderboard_by_belt'),
    path('trainee/<int:trainee_id>/points/', leaderboard_views.trainee_profile_points, name='trainee_profile_points'),
    path('belt-rank/progress/', leaderboard_views.belt_rank_progress, name='belt_rank_progress'),
    
    # Notification URLs
    path('notifications/', notification_views.notification_list, name='notification_list'),
    path('notifications/<int:notification_id>/mark-as-read/', notification_views.mark_as_read, name='mark_notification_read'),
    path('notifications/mark-all-as-read/', notification_views.mark_all_as_read, name='mark_all_notifications_read'),
    path('notifications/unread-count/', notification_views.get_unread_count, name='unread_count'),
    path('notifications/recent/', notification_views.get_recent_notifications, name='recent_notifications'),
]

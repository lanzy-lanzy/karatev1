"""
Core views package for BlackCobra Karate Club System.
"""
# Auth views
from core.views.auth import (
    home,
    redirect_to_dashboard,
    login_view,
    logout_view,
    register_view,
)

# Admin views
from core.views.admin import (
    dashboard_view,
    trainee_list,
    trainee_list_partial,
    trainee_add,
    trainee_edit,
    trainee_delete,
    event_list,
    event_list_partial,
    event_detail,
    event_add,
    event_edit,
    event_delete,
    event_status_update,
    matchmaking_list,
    matchmaking_list_partial,
    match_add,
    match_edit,
    match_delete,
    auto_matchmaking,
    auto_matchmaking_confirm,
    payment_list,
    payment_list_partial,
    payment_add,
    payment_edit,
    payment_delete,
    payment_mark_completed,
    reports_view,
    reports_export,
)

# Registration views
from core.views.admin_registrations import (
    registration_list,
    registration_detail,
    registration_approve,
    registration_reject,
)

# Trainee views
from core.views.trainee import (
    dashboard_view as trainee_dashboard_view,
    events_view as trainee_events_view,
    event_register as trainee_event_register,
    event_unregister as trainee_event_unregister,
    matches_view as trainee_matches_view,
    payments_view as trainee_payments_view,
)

from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def role_required(allowed_roles):
    """
    Decorator factory that restricts access to users with specific roles.
    
    Args:
        allowed_roles: A list of role strings that are allowed to access the view.
    
    Returns:
        A decorator that checks if the user has one of the allowed roles.
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required(login_url='/login/')
        def wrapper(request, *args, **kwargs):
            if hasattr(request.user, 'profile') and request.user.profile.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            return redirect('/login/')
        return wrapper
    return decorator


def admin_required(view_func):
    """Decorator ensuring user has admin role."""
    @wraps(view_func)
    @login_required(login_url='/login/')
    def wrapper(request, *args, **kwargs):
        if hasattr(request.user, 'profile') and request.user.profile.role == 'admin':
            return view_func(request, *args, **kwargs)
        return redirect('/login/')
    return wrapper


def trainee_required(view_func):
    """Decorator ensuring user has trainee role."""
    @wraps(view_func)
    @login_required(login_url='/login/')
    def wrapper(request, *args, **kwargs):
        if hasattr(request.user, 'profile') and request.user.profile.role == 'trainee':
            return view_func(request, *args, **kwargs)
        return redirect('/login/')
    return wrapper


def judge_required(view_func):
    """Decorator ensuring user has judge role."""
    @wraps(view_func)
    @login_required(login_url='/login/')
    def wrapper(request, *args, **kwargs):
        if hasattr(request.user, 'profile') and request.user.profile.role == 'judge':
            return view_func(request, *args, **kwargs)
        return redirect('/login/')
    return wrapper

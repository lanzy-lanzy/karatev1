"""
Authentication views for the BlackCobra Karate Club System.
Handles login, logout, and role-based redirects.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def home(request):
    """Home page - show landing page if not authenticated, else redirect to dashboard."""
    if request.user.is_authenticated:
        return redirect_to_dashboard(request.user)
    return render(request, 'landing.html')


def redirect_to_dashboard(user):
    """Redirect user to their role-specific dashboard."""
    if hasattr(user, 'profile'):
        return redirect(user.profile.get_dashboard_url())
    return redirect('/login/')


def login_view(request):
    """Handle user login with role-based redirect."""
    if request.user.is_authenticated:
        return redirect_to_dashboard(request.user)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect_to_dashboard(user)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'auth/login.html')


def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

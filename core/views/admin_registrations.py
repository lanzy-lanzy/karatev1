"""
Registration management views for admin.
Handles new member registrations requiring admin approval.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages

from core.decorators import admin_required
from core.models import Registration, UserProfile, Payment, Trainee


@admin_required
def registration_list(request):
    """
    List all pending registrations for admin review.
    """
    registrations = Registration.objects.all()
    
    # Search filter
    search_query = request.GET.get('search', '').strip()
    if search_query:
        registrations = registrations.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    # Status filter
    status_filter = request.GET.get('status', '').strip()
    if status_filter:
        registrations = registrations.filter(status=status_filter)
    
    # Payment status filter
    payment_status_filter = request.GET.get('payment_status', '').strip()
    if payment_status_filter:
        registrations = registrations.filter(payment_status=payment_status_filter)
    
    # Get stats
    context = {
        'registrations': registrations,
        'pending_count': Registration.objects.filter(status='pending').count(),
        'approved_count': Registration.objects.filter(status='approved').count(),
        'rejected_count': Registration.objects.filter(status='rejected').count(),
        'paid_count': Registration.objects.filter(payment_status='paid').count(),
    }
    
    return render(request, 'admin/registrations/list.html', context)


@admin_required
def registration_detail(request, registration_id):
    """
    Display detailed view of a registration with approval/rejection options.
    """
    registration = get_object_or_404(Registration, id=registration_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'mark_payment_paid':
            # Mark payment as paid for already approved registrations
            registration.payment_status = 'paid'
            registration.save()
            
            # Create payment record if it doesn't exist
            try:
                # Ensure UserProfile exists
                profile, _ = UserProfile.objects.get_or_create(
                    user=registration.user,
                    defaults={'role': 'trainee'}
                )
                
                # Ensure Trainee exists
                trainee, _ = Trainee.objects.get_or_create(
                    profile=profile,
                    defaults={
                        'belt_rank': registration.belt_level,
                        'weight': 0,
                        'emergency_contact': registration.first_name,
                        'emergency_phone': registration.phone,
                        'status': 'active'
                    }
                )
                
                # Create payment record if it doesn't exist
                existing_payment = Payment.objects.filter(
                    trainee=trainee,
                    payment_type='membership',
                    amount=registration.membership_fee
                ).first()
                
                if not existing_payment:
                    Payment.objects.create(
                        trainee=trainee,
                        amount=registration.membership_fee,
                        payment_type='membership',
                        payment_method='cash',
                        status='completed',
                        completed_at=timezone.now(),
                        notes=f'Membership fee paid during registration approval'
                    )
            except Exception as e:
                messages.warning(request, f'Error creating payment: {str(e)}')
            
            messages.success(request, f'Payment for {registration.first_name} {registration.last_name} has been marked as paid!')
            return redirect('admin_registration_detail', registration_id=registration.id)
        
        elif action == 'approve':
            # Mark payment as paid if checkbox is checked
            if request.POST.get('mark_payment'):
                registration.payment_status = 'paid'
            
            registration.status = 'approved'
            registration.reviewed_by = request.user
            registration.reviewed_at = timezone.now()
            registration.save()
            
            messages.success(request, f'{registration.first_name} {registration.last_name} has been approved!')
            
            # Create UserProfile and Trainee for approved registration
            try:
                # Create or get UserProfile
                profile, created = UserProfile.objects.get_or_create(
                    user=registration.user,
                    defaults={'role': 'trainee'}
                )
                
                # Create or get Trainee record
                trainee, trainee_created = Trainee.objects.get_or_create(
                    profile=profile,
                    defaults={
                        'belt_rank': registration.belt_level,
                        'weight': 0,
                        'emergency_contact': registration.first_name,
                        'emergency_phone': registration.phone,
                        'status': 'active'
                    }
                )
                
                # Create payment record if payment is marked as paid
                if registration.payment_status == 'paid':
                    existing_payment = Payment.objects.filter(
                        trainee=trainee,
                        payment_type='membership',
                        amount=registration.membership_fee
                    ).first()
                    
                    if not existing_payment:
                        Payment.objects.create(
                            trainee=trainee,
                            amount=registration.membership_fee,
                            payment_type='membership',
                            payment_method='cash',
                            status='completed',
                            completed_at=timezone.now(),
                            notes=f'Membership fee paid during registration approval'
                        )
            except Exception as e:
                messages.warning(request, f'Error creating profile/payment: {str(e)}')
            
            return redirect('admin_registrations')
        
        elif action == 'reject':
            rejection_reason = request.POST.get('rejection_reason', '').strip()
            registration.status = 'rejected'
            registration.rejection_reason = rejection_reason
            registration.reviewed_by = request.user
            registration.reviewed_at = timezone.now()
            registration.save()
            
            messages.success(request, f'{registration.first_name} {registration.last_name}\'s registration has been rejected.')
            return redirect('admin_registrations')
    
    # Fetch associated payment if exists
    payment = None
    try:
        if hasattr(registration.user, 'profile') and hasattr(registration.user.profile, 'trainee'):
            payment = Payment.objects.filter(
                trainee=registration.user.profile.trainee,
                payment_type='membership',
                amount=registration.membership_fee
            ).first()
    except:
        pass
    
    context = {
        'registration': registration,
        'payment': payment,
    }
    
    return render(request, 'admin/registrations/detail.html', context)


@admin_required
def registration_approve(request, registration_id):
    """
    Quick approve endpoint for registrations.
    """
    registration = get_object_or_404(Registration, id=registration_id)
    
    if request.method == 'POST':
        registration.status = 'approved'
        registration.reviewed_by = request.user
        registration.reviewed_at = timezone.now()
        registration.save()
        
        # Create UserProfile if not exists
        try:
            if not hasattr(registration.user, 'profile'):
                UserProfile.objects.create(
                    user=registration.user,
                    role='trainee'
                )
        except:
            pass
        
        messages.success(request, f'{registration.first_name} {registration.last_name} has been approved!')
    
    return redirect('admin_registrations')


@admin_required
def registration_reject(request, registration_id):
    """
    Quick reject endpoint for registrations.
    """
    registration = get_object_or_404(Registration, id=registration_id)
    
    if request.method == 'POST':
        registration.status = 'rejected'
        registration.reviewed_by = request.user
        registration.reviewed_at = timezone.now()
        registration.save()
        
        messages.success(request, f'{registration.first_name} {registration.last_name}\'s registration has been rejected.')
    
    return redirect('admin_registrations')

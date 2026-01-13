from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from ..models import Trainee, Attendance
from datetime import datetime, date

@login_required
def attendance_dashboard(request):
    """
    Overview of attendance.
    """
    from django.db.models import Count, Q
    
    today = timezone.now().date()
    
    # 1. Active Trainees
    active_trainees_count = Trainee.objects.filter(status='active').count()
    
    # 2. Today's Attendance
    todays_attendance_count = Attendance.objects.filter(
        date=today, 
        status='present'
    ).count()
    
    # Check if attendance has been marked for today
    today_marked = Attendance.objects.filter(date=today).exists()
    todays_attendance_display = todays_attendance_count if today_marked else "--"
    
    # 3. Average Attendance (Global)
    total_records = Attendance.objects.count()
    if total_records > 0:
        total_present = Attendance.objects.filter(status='present').count()
        average_attendance = int((total_present / total_records) * 100)
    else:
        average_attendance = 0
        
    # 4. Recent Activity (Group by Date)
    # Get distinct dates from last 10 days
    recent_dates = Attendance.objects.values('date').distinct().order_by('-date')[:5]
    
    recent_activity = []
    for entry in recent_dates:
        d = entry['date']
        present = Attendance.objects.filter(date=d, status='present').count()
        total = Attendance.objects.filter(date=d).count()
        rate = int((present / total) * 100) if total > 0 else 0
        
        recent_activity.append({
            'date': d,
            'present': present,
            'total': total,
            'rate': rate
        })
    
    context = {
        'active_trainees_count': active_trainees_count,
        'todays_attendance': todays_attendance_display,
        'average_attendance': average_attendance,
        'recent_activity': recent_activity,
        'today_marked': today_marked,
    }
    
    return render(request, 'admin/attendance/dashboard.html', context)

@login_required
def attendance_mark(request):
    """
    View to mark attendance for a day.
    """
    if request.method == 'POST':
        date_str = request.POST.get('date')
        attendance_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Process attendance
        trainees = Trainee.objects.filter(status='active')
        attendance_count = 0
        for trainee in trainees:
            status = request.POST.get(f'status_{trainee.id}')
            notes = request.POST.get(f'notes_{trainee.id}', '')
            
            if status:
                Attendance.objects.update_or_create(
                    trainee=trainee,
                    date=attendance_date,
                    defaults={
                        'status': status,
                        'notes': notes
                    }
                )
                if status == 'present':
                    attendance_count += 1
        
        # Clear any query cache
        from django.core.cache import cache
        cache.clear()
        
        messages.success(request, f"Attendance marked for {attendance_date.strftime('%B %d, %Y')} ({attendance_count} present)")
        return redirect('attendance_dashboard')

    today_str = request.GET.get('date', timezone.now().date().isoformat())
    try:
        current_date = datetime.strptime(today_str, '%Y-%m-%d').date()
    except ValueError:
        current_date = timezone.now().date()
        today_str = current_date.isoformat()

    # Get trainees as a list so we can annotate them
    trainees = list(Trainee.objects.filter(status='active').order_by('profile__user__last_name'))
    
    # Fetch existing attendance for this date
    attendance_records = Attendance.objects.filter(date=current_date)
    attendance_map = {att.trainee_id: att for att in attendance_records}
    
    # Attach attendance record to each trainee
    for trainee in trainees:
        trainee.attendance_record = attendance_map.get(trainee.id)
    
    return render(request, 'admin/attendance/mark.html', {
        'trainees': trainees,
        'today': today_str,
        'attendance_map': attendance_map
    })

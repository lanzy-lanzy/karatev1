"""
Report Service for the BlackCobra Karate Club System.
Handles report generation for membership, financial, and event reports.
Requirements: 7.1, 7.2, 7.3, 7.4
"""
import csv
import io
from datetime import date
from decimal import Decimal
from typing import Any, Dict

from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncMonth

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
import os
from django.conf import settings


class ReportService:
    """
    Service class for generating various reports.
    Requirements: 7.1, 7.2, 7.3, 7.4
    """
    
    def membership_report(self, start_date: date, end_date: date) -> Dict[str, Any]:
        """
        Generate membership statistics report.
        Requirements: 7.1
        
        Returns:
            dict containing:
            - total_members: Total number of trainees
            - active_members: Number of active trainees
            - inactive_members: Number of inactive trainees
            - suspended_members: Number of suspended trainees
            - new_members: Number of trainees who joined in date range
            - members_by_belt: Breakdown by belt rank
            - members_by_weight_class: Breakdown by weight class
        """
        from core.models import Trainee
        
        # Get all trainees
        all_trainees = Trainee.objects.all()
        
        # Basic counts
        total_members = all_trainees.count()
        active_members = all_trainees.filter(status='active').count()
        inactive_members = all_trainees.filter(status='inactive').count()
        suspended_members = all_trainees.filter(status='suspended').count()
        
        # New members in date range
        new_members = all_trainees.filter(
            joined_date__gte=start_date,
            joined_date__lte=end_date
        ).count()

        # Members by belt rank with detailed list
        members_by_belt = list(
            all_trainees.values('belt_rank')
            .annotate(count=Count('id'))
            .order_by('belt_rank')
        )
        
        # Get detailed member list by belt rank with names
        belt_rank_details = {}
        for trainee in all_trainees.select_related('profile__user').order_by('belt_rank', 'profile__user__first_name'):
            belt = trainee.belt_rank or 'Unknown'
            if belt not in belt_rank_details:
                belt_rank_details[belt] = []
            name = f"{trainee.profile.user.first_name} {trainee.profile.user.last_name}"
            belt_rank_details[belt].append({
                'name': name,
                'status': trainee.status,
                'weight_class': trainee.weight_class or 'N/A'
            })
        
        # Members by weight class
        members_by_weight_class = list(
            all_trainees.values('weight_class')
            .annotate(count=Count('id'))
            .order_by('weight_class')
        )
        
        return {
            'report_type': 'membership',
            'start_date': start_date,
            'end_date': end_date,
            'total_members': total_members,
            'active_members': active_members,
            'inactive_members': inactive_members,
            'suspended_members': suspended_members,
            'new_members': new_members,
            'members_by_belt': members_by_belt,
            'belt_rank_details': belt_rank_details,
            'members_by_weight_class': members_by_weight_class,
        }
    
    def financial_report(self, start_date: date, end_date: date) -> Dict[str, Any]:
        """
        Generate financial summary report.
        Requirements: 7.2, 7.4
        
        Returns:
            dict containing:
            - total_revenue: Total completed payments
            - pending_amount: Total pending payments
            - overdue_amount: Total overdue payments
            - payments_by_type: Breakdown by payment type
            - payments_by_month: Monthly breakdown
            - outstanding_balances: List of trainees with pending/overdue payments
        """
        from core.models import Payment
        from django.utils import timezone
        from datetime import datetime
        
        # Convert dates to datetime for filtering
        start_datetime = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
        end_datetime = timezone.make_aware(datetime.combine(end_date, datetime.max.time()))
        
        # Get payments in date range
        payments_in_range = Payment.objects.filter(
            payment_date__gte=start_datetime,
            payment_date__lte=end_datetime
        )
        
        # Total revenue (completed payments)
        total_revenue = payments_in_range.filter(
            status='completed'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        # Pending amount
        pending_amount = payments_in_range.filter(
            status='pending'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        # Overdue amount
        overdue_amount = payments_in_range.filter(
            status='overdue'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        # Payments by type
        payments_by_type = list(
            payments_in_range.filter(status='completed')
            .values('payment_type')
            .annotate(total=Sum('amount'), count=Count('id'))
            .order_by('payment_type')
        )
        
        # Payments by month
        payments_by_month = list(
            payments_in_range.filter(status='completed')
            .annotate(month=TruncMonth('payment_date'))
            .values('month')
            .annotate(total=Sum('amount'), count=Count('id'))
            .order_by('month')
        )
        
        # Outstanding balances (trainees with pending/overdue payments)
        outstanding_balances = list(
            Payment.objects.filter(
                status__in=['pending', 'overdue']
            ).values(
                'trainee__id',
                'trainee__profile__user__first_name',
                'trainee__profile__user__last_name'
            ).annotate(
                total_outstanding=Sum('amount')
            ).order_by('-total_outstanding')[:20]
        )
        
        return {
            'report_type': 'financial',
            'start_date': start_date,
            'end_date': end_date,
            'total_revenue': total_revenue,
            'pending_amount': pending_amount,
            'overdue_amount': overdue_amount,
            'payments_by_type': payments_by_type,
            'payments_by_month': payments_by_month,
            'outstanding_balances': outstanding_balances,
        }
    
    def event_report(self, event_id: int) -> Dict[str, Any]:
        """
        Generate event participation report.
        Requirements: 7.1, 7.2
        
        Returns:
            dict containing:
            - event: Event details
            - total_registrations: Number of registrations
            - participants_by_belt: Breakdown by belt rank with trainee names
            - participants_by_weight_class: Breakdown by weight class with trainee names
            - matches_summary: Match statistics
            - all_participants: List of all trainees with their details
        """
        from core.models import Event, EventRegistration, Match, MatchResult
        
        event = Event.objects.get(id=event_id)
        
        # Get registrations
        registrations = EventRegistration.objects.filter(
            event=event,
            status='registered'
        ).select_related('trainee', 'trainee__profile', 'trainee__profile__user')
        
        total_registrations = registrations.count()
        
        # Get all participants with trainee names
        all_participants = []
        for reg in registrations:
            trainee = reg.trainee
            user = trainee.profile.user
            all_participants.append({
                'id': trainee.id,
                'name': f"{user.first_name} {user.last_name}".strip() or user.username,
                'belt_rank': trainee.belt_rank,
                'weight_class': trainee.weight_class,
            })
        
        # Participants by belt rank with trainee names
        participants_by_belt = {}
        for participant in all_participants:
            belt = participant['belt_rank'] or 'Unknown'
            if belt not in participants_by_belt:
                participants_by_belt[belt] = {
                    'count': 0,
                    'names': []
                }
            participants_by_belt[belt]['count'] += 1
            participants_by_belt[belt]['names'].append(participant['name'])
        
        # Convert to list format for template
        participants_by_belt_list = [
            {
                'belt_rank': belt,
                'count': data['count'],
                'names': ', '.join(sorted(data['names']))
            }
            for belt, data in sorted(participants_by_belt.items())
        ]
        
        # Participants by weight class with trainee names
        participants_by_weight_class = {}
        for participant in all_participants:
            weight = participant['weight_class'] or 'Unknown'
            if weight not in participants_by_weight_class:
                participants_by_weight_class[weight] = {
                    'count': 0,
                    'names': []
                }
            participants_by_weight_class[weight]['count'] += 1
            participants_by_weight_class[weight]['names'].append(participant['name'])
        
        # Convert to list format for template
        participants_by_weight_class_list = [
            {
                'weight_class': weight,
                'count': data['count'],
                'names': ', '.join(sorted(data['names']))
            }
            for weight, data in sorted(participants_by_weight_class.items())
        ]
        
        # Match statistics
        matches = Match.objects.filter(event=event)
        total_matches = matches.count()
        completed_matches = matches.filter(status='completed').count()
        scheduled_matches = matches.filter(status='scheduled').count()
        
        return {
            'report_type': 'event',
            'event': {
                'id': event.id,
                'name': event.name,
                'event_date': event.event_date,
                'location': event.location,
                'status': event.status,
                'max_participants': event.max_participants,
            },
            'total_registrations': total_registrations,
            'participants_by_belt': participants_by_belt_list,
            'participants_by_weight_class': participants_by_weight_class_list,
            'matches_summary': {
                'total': total_matches,
                'completed': completed_matches,
                'scheduled': scheduled_matches,
            },
            'all_participants': all_participants,
        }

    
    def export_pdf(self, report_data: Dict[str, Any], report_type: str) -> bytes:
        """
        Export report as PDF.
        Supports: membership, financial, event, trainee_list
        Requirements: 7.3
        
        Args:
            report_data: The report data dictionary
            report_type: Type of report ('membership', 'financial', 'event', 'trainee_list')
            
        Returns:
            PDF file as bytes
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        styles = getSampleStyleSheet()
        elements = []
        
        # Title style
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=12,
            fontName='Helvetica-Bold'
        )
        
        if report_type == 'membership':
            elements = self._build_membership_pdf(report_data, styles, title_style)
        elif report_type == 'financial':
            elements = self._build_financial_pdf(report_data, styles, title_style)
        elif report_type == 'event':
            elements = self._build_event_pdf(report_data, styles, title_style)
        elif report_type == 'trainee_list':
            elements = self._build_trainee_list_pdf(report_data, styles, title_style)
        
        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
    
    def _build_membership_pdf(self, data: dict, styles, title_style) -> list:
        """Build PDF elements for membership report."""
        elements = []
        
        # Add header with logos and organization name
        logo_path = os.path.join(settings.BASE_DIR, 'core', 'static', 'images', 'black_cobra_logo.jpg')
        judo_logo_path = os.path.join(settings.BASE_DIR, 'core', 'static', 'images', 'judo_logo.png')
        
        # Create header table with left logo, center text, right logo
        header_data = [[None, None, None]]
        
        # Left logo
        if os.path.exists(logo_path):
            left_logo = Image(logo_path, width=1*inch, height=1*inch)
            header_data[0][0] = left_logo
        
        # Center text
        header_style = ParagraphStyle(
            'OrgHeader',
            parent=styles['Heading2'],
            fontSize=13,
            textColor=colors.black,
            alignment=1,  # Center alignment
            leading=16
        )
        center_text = Paragraph("BLACK COBRA JUDO<br/>KARATE AIKIDO<br/>ASSOCIATION OF THE<br/>PHILIPPINES", header_style)
        header_data[0][1] = center_text
        
        # Right logo
        if os.path.exists(judo_logo_path):
            right_logo = Image(judo_logo_path, width=1*inch, height=1*inch)
            header_data[0][2] = right_logo
        else:
            # Placeholder if judo logo doesn't exist
            header_data[0][2] = Paragraph("Judo<br/>Logo", styles['Normal'])
        
        header_table = Table(header_data, colWidths=[1.2*inch, 3.6*inch, 1.2*inch])
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (0, -1), 0),
            ('RIGHTPADDING', (-1, 0), (-1, -1), 0),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 15))
        
        # Title
        elements.append(Paragraph("Membership Report", title_style))
        elements.append(Paragraph(
            f"Period: {data['start_date']} to {data['end_date']}", 
            styles['Normal']
        ))
        elements.append(Spacer(1, 20))
        
        # Summary table
        summary_data = [
            ['Metric', 'Count'],
            ['Total Members', str(data['total_members'])],
            ['Active Members', str(data['active_members'])],
            ['Inactive Members', str(data['inactive_members'])],
            ['Suspended Members', str(data['suspended_members'])],
            ['New Members (Period)', str(data['new_members'])],
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 20))
        
        # Belt rank breakdown with trainee names
        if data.get('belt_rank_details'):
            elements.append(Paragraph("Members by Belt Rank - Detailed", styles['Heading2']))
            elements.append(Spacer(1, 10))
            
            for belt_rank in sorted(data['belt_rank_details'].keys()):
                members = data['belt_rank_details'][belt_rank]
                
                # Belt rank section header
                elements.append(Paragraph(f"{belt_rank.title()} ({len(members)})", styles['Heading3']))
                
                # Members list for this belt
                member_data = [['Name', 'Status', 'Weight Class']]
                for member in members:
                    member_data.append([
                        member['name'],
                        member['status'].title(),
                        member['weight_class']
                    ])
                
                member_table = Table(member_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
                member_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('ALIGN', (1, 0), (2, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
                ]))
                elements.append(member_table)
                elements.append(Spacer(1, 10))
        
        # Add signatory section at the end
        elements.append(Spacer(1, 40))
        elements.append(Paragraph("Prepared By:", styles['Normal']))
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("_" * 40, styles['Normal']))
        elements.append(Paragraph("INSTRUCTOR", styles['Normal']))
        
        return elements
    
    def _build_financial_pdf(self, data: dict, styles, title_style) -> list:
        """Build PDF elements for financial report."""
        elements = []
        
        # Add header with logos and organization name
        logo_path = os.path.join(settings.BASE_DIR, 'core', 'static', 'images', 'black_cobra_logo.jpg')
        judo_logo_path = os.path.join(settings.BASE_DIR, 'core', 'static', 'images', 'judo_logo.png')
        
        # Create header table with left logo, center text, right logo
        header_data = [[None, None, None]]
        
        # Left logo
        if os.path.exists(logo_path):
            left_logo = Image(logo_path, width=1*inch, height=1*inch)
            header_data[0][0] = left_logo
        
        # Center text
        header_style = ParagraphStyle(
            'OrgHeader',
            parent=styles['Heading2'],
            fontSize=13,
            textColor=colors.black,
            alignment=1,  # Center alignment
            leading=16
        )
        center_text = Paragraph("BLACK COBRA JUDO<br/>KARATE AIKIDO<br/>ASSOCIATION OF THE<br/>PHILIPPINES", header_style)
        header_data[0][1] = center_text
        
        # Right logo
        if os.path.exists(judo_logo_path):
            right_logo = Image(judo_logo_path, width=1*inch, height=1*inch)
            header_data[0][2] = right_logo
        else:
            # Placeholder if judo logo doesn't exist
            header_data[0][2] = Paragraph("Judo<br/>Logo", styles['Normal'])
        
        header_table = Table(header_data, colWidths=[1.2*inch, 3.6*inch, 1.2*inch])
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (0, -1), 0),
            ('RIGHTPADDING', (-1, 0), (-1, -1), 0),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 15))
        
        # Title
        elements.append(Paragraph("Financial Report", title_style))
        elements.append(Paragraph(
            f"Period: {data['start_date']} to {data['end_date']}", 
            styles['Normal']
        ))
        elements.append(Spacer(1, 20))
        
        # Summary table
        summary_data = [
            ['Metric', 'Amount'],
            ['Total Revenue', f"${data['total_revenue']:.2f}"],
            ['Pending Payments', f"${data['pending_amount']:.2f}"],
            ['Overdue Payments', f"${data['overdue_amount']:.2f}"],
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 20))
        
        # Payments by type
        if data['payments_by_type']:
            elements.append(Paragraph("Revenue by Payment Type", styles['Heading2']))
            type_data = [['Payment Type', 'Count', 'Total']]
            for item in data['payments_by_type']:
                type_data.append([
                    item['payment_type'].title(),
                    str(item['count']),
                    f"${item['total']:.2f}"
                ])
            
            type_table = Table(type_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
            type_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(type_table)
            elements.append(Spacer(1, 20))
        
        # Outstanding balances
        if data['outstanding_balances']:
            elements.append(Paragraph("Outstanding Balances", styles['Heading2']))
            balance_data = [['Trainee', 'Outstanding Amount']]
            for item in data['outstanding_balances']:
                name = f"{item['trainee__profile__user__first_name']} {item['trainee__profile__user__last_name']}"
                balance_data.append([name, f"${item['total_outstanding']:.2f}"])
            
            balance_table = Table(balance_data, colWidths=[3*inch, 2*inch])
            balance_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(balance_table)
        
        # Add signatory section at the end
        elements.append(Spacer(1, 40))
        elements.append(Paragraph("Prepared By:", styles['Normal']))
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("_" * 40, styles['Normal']))
        elements.append(Paragraph("INSTRUCTOR", styles['Normal']))
        
        return elements
    
    def _build_event_pdf(self, data: dict, styles, title_style) -> list:
        """Build PDF elements for event report."""
        elements = []
        
        # Add header with logos and organization name
        logo_path = os.path.join(settings.BASE_DIR, 'core', 'static', 'images', 'black_cobra_logo.jpg')
        judo_logo_path = os.path.join(settings.BASE_DIR, 'core', 'static', 'images', 'judo_logo.png')
        
        # Create header table with left logo, center text, right logo
        header_data = [[None, None, None]]
        
        # Left logo
        if os.path.exists(logo_path):
            left_logo = Image(logo_path, width=1*inch, height=1*inch)
            header_data[0][0] = left_logo
        
        # Center text
        header_style = ParagraphStyle(
            'OrgHeader',
            parent=styles['Heading2'],
            fontSize=13,
            textColor=colors.black,
            alignment=1,  # Center alignment
            leading=16
        )
        center_text = Paragraph("BLACK COBRA JUDO<br/>KARATE AIKIDO<br/>ASSOCIATION OF THE<br/>PHILIPPINES", header_style)
        header_data[0][1] = center_text
        
        # Right logo
        if os.path.exists(judo_logo_path):
            right_logo = Image(judo_logo_path, width=1*inch, height=1*inch)
            header_data[0][2] = right_logo
        else:
            # Placeholder if judo logo doesn't exist
            header_data[0][2] = Paragraph("Judo<br/>Logo", styles['Normal'])
        
        header_table = Table(header_data, colWidths=[1.2*inch, 3.6*inch, 1.2*inch])
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (0, -1), 0),
            ('RIGHTPADDING', (-1, 0), (-1, -1), 0),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 15))
        
        event = data['event']
        
        # Title
        elements.append(Paragraph(f"Event Report: {event['name']}", title_style))
        elements.append(Paragraph(
            f"Date: {event['event_date']} | Location: {event['location']}", 
            styles['Normal']
        ))
        elements.append(Spacer(1, 20))
        
        # Summary table
        summary_data = [
            ['Metric', 'Value'],
            ['Status', event['status'].title()],
            ['Max Participants', str(event['max_participants'])],
            ['Total Registrations', str(data['total_registrations'])],
            ['Total Matches', str(data['matches_summary']['total'])],
            ['Completed Matches', str(data['matches_summary']['completed'])],
            ['Scheduled Matches', str(data['matches_summary']['scheduled'])],
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 20))
        
        # Participants by belt
        if data['participants_by_belt']:
            elements.append(Paragraph("Participants by Belt Rank", styles['Heading2']))
            belt_data = [['Belt Rank', 'Count', 'Trainees']]
            for item in data['participants_by_belt']:
                belt_data.append([
                    item.get('belt_rank', 'Unknown').title() if item.get('belt_rank') else 'Unknown',
                    str(item['count']),
                    item.get('names', '')
                ])
            
            belt_table = Table(belt_data, colWidths=[1.5*inch, 1*inch, 2.5*inch])
            belt_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (1, -1), 'CENTER'),
                ('ALIGN', (2, 0), (2, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            elements.append(belt_table)
        
        # Participants by weight class
        if data['participants_by_weight_class']:
            elements.append(Spacer(1, 20))
            elements.append(Paragraph("Participants by Weight Class", styles['Heading2']))
            weight_data = [['Weight Class', 'Count', 'Trainees']]
            for item in data['participants_by_weight_class']:
                weight_data.append([
                    item.get('weight_class', 'Unknown'),
                    str(item['count']),
                    item.get('names', '')
                ])
            
            weight_table = Table(weight_data, colWidths=[1.5*inch, 1*inch, 2.5*inch])
            weight_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (1, -1), 'CENTER'),
                ('ALIGN', (2, 0), (2, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            elements.append(weight_table)
        
        # Add signatory section at the end
        elements.append(Spacer(1, 40))
        elements.append(Paragraph("Prepared By:", styles['Normal']))
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("_" * 40, styles['Normal']))
        elements.append(Paragraph("INSTRUCTOR", styles['Normal']))
        
        return elements

    
    def export_csv(self, report_data: Dict[str, Any], report_type: str) -> str:
        """
        Export report as CSV.
        Supports: membership, financial, event, trainee_list
        Requirements: 7.3
        
        Args:
            report_data: The report data dictionary
            report_type: Type of report ('membership', 'financial', 'event', 'trainee_list')
            
        Returns:
            CSV content as string
        """
        output = io.StringIO()
        
        if report_type == 'membership':
            self._build_membership_csv(output, report_data)
        elif report_type == 'financial':
            self._build_financial_csv(output, report_data)
        elif report_type == 'event':
            self._build_event_csv(output, report_data)
        elif report_type == 'trainee_list':
            self._build_trainee_list_csv(output, report_data)
        
        return output.getvalue()
    
    def _build_membership_csv(self, output: io.StringIO, data: dict) -> None:
        """Build CSV content for membership report."""
        writer = csv.writer(output)
        
        # Header
        writer.writerow(['Membership Report'])
        writer.writerow([f"Period: {data['start_date']} to {data['end_date']}"])
        writer.writerow([])
        
        # Summary
        writer.writerow(['Summary'])
        writer.writerow(['Metric', 'Count'])
        writer.writerow(['Total Members', data['total_members']])
        writer.writerow(['Active Members', data['active_members']])
        writer.writerow(['Inactive Members', data['inactive_members']])
        writer.writerow(['Suspended Members', data['suspended_members']])
        writer.writerow(['New Members (Period)', data['new_members']])
        writer.writerow([])
        
        # Belt breakdown with trainee names
        writer.writerow(['Members by Belt Rank - Detailed'])
        writer.writerow([])
        
        if data.get('belt_rank_details'):
            for belt_rank in sorted(data['belt_rank_details'].keys()):
                members = data['belt_rank_details'][belt_rank]
                writer.writerow([f"{belt_rank.title()} ({len(members)})"])
                writer.writerow(['Name', 'Status', 'Weight Class'])
                for member in members:
                    writer.writerow([
                        member['name'],
                        member['status'].title(),
                        member['weight_class']
                    ])
                writer.writerow([])
        else:
            # Fallback to summary if detailed list not available
            writer.writerow(['Belt Rank', 'Count'])
            for item in data['members_by_belt']:
                writer.writerow([item['belt_rank'].title(), item['count']])
            writer.writerow([])
        
        # Weight class breakdown
        writer.writerow(['Members by Weight Class'])
        writer.writerow(['Weight Class', 'Count'])
        for item in data['members_by_weight_class']:
            writer.writerow([item['weight_class'], item['count']])
    
    def _build_financial_csv(self, output: io.StringIO, data: dict) -> None:
        """Build CSV content for financial report."""
        writer = csv.writer(output)
        
        # Header
        writer.writerow(['Financial Report'])
        writer.writerow([f"Period: {data['start_date']} to {data['end_date']}"])
        writer.writerow([])
        
        # Summary
        writer.writerow(['Summary'])
        writer.writerow(['Metric', 'Amount'])
        writer.writerow(['Total Revenue', f"${data['total_revenue']:.2f}"])
        writer.writerow(['Pending Payments', f"${data['pending_amount']:.2f}"])
        writer.writerow(['Overdue Payments', f"${data['overdue_amount']:.2f}"])
        writer.writerow([])
        
        # Payments by type
        writer.writerow(['Revenue by Payment Type'])
        writer.writerow(['Payment Type', 'Count', 'Total'])
        for item in data['payments_by_type']:
            writer.writerow([
                item['payment_type'].title(),
                item['count'],
                f"${item['total']:.2f}"
            ])
        writer.writerow([])
        
        # Outstanding balances
        writer.writerow(['Outstanding Balances'])
        writer.writerow(['Trainee', 'Outstanding Amount'])
        for item in data['outstanding_balances']:
            name = f"{item['trainee__profile__user__first_name']} {item['trainee__profile__user__last_name']}"
            writer.writerow([name, f"${item['total_outstanding']:.2f}"])
    
    def _build_event_csv(self, output: io.StringIO, data: dict) -> None:
          """Build CSV content for event report."""
          writer = csv.writer(output)
          event = data['event']
          
          # Header
          writer.writerow(['Event Report'])
          writer.writerow([f"Event: {event['name']}"])
          writer.writerow([f"Date: {event['event_date']}"])
          writer.writerow([f"Location: {event['location']}"])
          writer.writerow([])
          
          # Summary
          writer.writerow(['Summary'])
          writer.writerow(['Metric', 'Value'])
          writer.writerow(['Status', event['status'].title()])
          writer.writerow(['Max Participants', event['max_participants']])
          writer.writerow(['Total Registrations', data['total_registrations']])
          writer.writerow(['Total Matches', data['matches_summary']['total']])
          writer.writerow(['Completed Matches', data['matches_summary']['completed']])
          writer.writerow(['Scheduled Matches', data['matches_summary']['scheduled']])
          writer.writerow([])
          
          # Participants by belt
          writer.writerow(['Participants by Belt Rank'])
          writer.writerow(['Belt Rank', 'Count', 'Trainees'])
          for item in data['participants_by_belt']:
              belt = item.get('belt_rank', 'Unknown').title() if item.get('belt_rank') else 'Unknown'
              names = item.get('names', '')
              writer.writerow([belt, item['count'], names])
          writer.writerow([])
          
          # Participants by weight class
          writer.writerow(['Participants by Weight Class'])
          writer.writerow(['Weight Class', 'Count', 'Trainees'])
          for item in data['participants_by_weight_class']:
              weight = item.get('weight_class', 'Unknown')
              names = item.get('names', '')
              writer.writerow([weight, item['count'], names])
          writer.writerow([])
          
          # All participants detailed list
          if data.get('all_participants'):
              writer.writerow(['All Participants - Detailed List'])
              writer.writerow(['Name', 'Belt Rank', 'Weight Class'])
              for participant in sorted(data['all_participants'], key=lambda x: x['name']):
                  writer.writerow([
                      participant['name'],
                      participant['belt_rank'] or 'Unknown',
                      participant['weight_class'] or 'Unknown'
                  ])

    def trainee_report(self, status_filter: str = None, belt_filter: str = None, trainee_ids: list = None, export_format: str = 'by_user') -> Dict[str, Any]:
        """
        Generate trainee listing report with optional filters.
        
        Args:
            status_filter: Filter by status (active, inactive, suspended)
            belt_filter: Filter by belt rank
            trainee_ids: List of specific trainee IDs to export
            export_format: 'by_user' (list format) or 'by_belt' (grouped by belt)
            
        Returns:
            dict containing trainee listing data
        """
        from core.models import Trainee
        
        trainees = Trainee.objects.select_related('profile__user').filter(archived=False)
        
        # Apply specific trainee ID filter if provided
        if trainee_ids:
            trainees = trainees.filter(id__in=trainee_ids)
        
        # Apply filters
        if status_filter:
            trainees = trainees.filter(status=status_filter)
        if belt_filter:
            trainees = trainees.filter(belt_rank=belt_filter)
        
        # Order by name
        trainees = trainees.order_by('profile__user__first_name', 'profile__user__last_name')
        
        # Build trainee list with details
        trainee_list = []
        for trainee in trainees:
            user = trainee.profile.user
            trainee_list.append({
                'id': trainee.id,
                'name': f"{user.first_name} {user.last_name}".strip() or user.username,
                'email': user.email,
                'belt_rank': trainee.belt_rank or 'Not Set',
                'weight_class': trainee.weight_class or 'Not Set',
                'age': trainee.age if hasattr(trainee, 'age') and trainee.age is not None else 'N/A',
                'status': trainee.status.title(),
                'join_date': trainee.joined_date,
            })
        
        # Group by belt rank if requested
        trainees_by_belt = {}
        if export_format == 'by_belt':
            for trainee in trainee_list:
                belt = trainee['belt_rank']
                if belt not in trainees_by_belt:
                    trainees_by_belt[belt] = []
                trainees_by_belt[belt].append(trainee)
        
        # Summary statistics
        return {
            'report_type': 'trainee_list',
            'export_format': export_format,
            'generated_date': date.today(),
            'total_trainees': len(trainee_list),
            'active_trainees': sum(1 for t in trainee_list if 'active' in t['status'].lower()),
            'inactive_trainees': sum(1 for t in trainee_list if 'inactive' in t['status'].lower()),
            'suspended_trainees': sum(1 for t in trainee_list if 'suspended' in t['status'].lower()),
            'status_filter': status_filter or 'All',
            'belt_filter': belt_filter or 'All',
            'trainees': trainee_list,
            'trainees_by_belt': trainees_by_belt,
        }
    
    def _build_trainee_list_pdf(self, data: dict, styles, title_style) -> list:
        """Build PDF elements for trainee list report."""
        export_format = data.get('export_format', 'by_user')
        
        if export_format == 'by_belt':
            return self._build_trainee_by_belt_pdf(data, styles, title_style)
        else:
            return self._build_trainee_by_user_pdf(data, styles, title_style)
    
    def _build_trainee_by_user_pdf(self, data: dict, styles, title_style) -> list:
        """Build PDF elements for trainee list organized by user."""
        elements = []
        
        # Header
        elements.append(Paragraph("BlackCobra Karate Club", title_style))
        elements.append(Paragraph("Trainee Management Report", styles['Heading2']))
        elements.append(Paragraph(
            f"Generated: {data['generated_date'].strftime('%B %d, %Y')} | "
            f"Status Filter: {data['status_filter']} | Belt Filter: {data['belt_filter']}",
            styles['Normal']
        ))
        elements.append(Spacer(1, 20))
        
        # Summary statistics
        summary_data = [
            ['Metric', 'Count'],
            ['Total Trainees', str(data['total_trainees'])],
            ['Active', str(data['active_trainees'])],
            ['Inactive', str(data['inactive_trainees'])],
            ['Suspended', str(data['suspended_trainees'])],
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc2626')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f3f4f6')),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 20))
        
        # Trainee list table
        if data['trainees']:
            elements.append(Paragraph("Trainee Details (By User)", styles['Heading3']))
            elements.append(Spacer(1, 10))
            
            table_data = [['Name', 'Email', 'Belt Rank', 'Weight Class', 'Age', 'Status', 'Joined']]
            
            for trainee in data['trainees']:
                join_date = trainee['join_date'].strftime('%m/%d/%Y') if trainee['join_date'] else 'N/A'
                table_data.append([
                    trainee['name'],
                    trainee['email'],
                    trainee['belt_rank'],
                    trainee['weight_class'],
                    str(trainee['age']),
                    trainee['status'],
                    join_date,
                ])
            
            # Adjust column widths for 7 columns
            trainee_table = Table(table_data, colWidths=[1.2*inch, 1.3*inch, 1*inch, 1*inch, 0.6*inch, 0.9*inch, 0.8*inch])
            trainee_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2937')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('ALIGN', (0, 0), (1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 5),
                ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ]))
            elements.append(trainee_table)
        else:
            elements.append(Paragraph("No trainees found matching the selected filters.", styles['Normal']))
        
        # Footer
        elements.append(Spacer(1, 40))
        elements.append(Paragraph("_" * 80, styles['Normal']))
        elements.append(Paragraph("Authorized By:", styles['Normal']))
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("_" * 40, styles['Normal']))
        elements.append(Paragraph("Admin Signature", styles['Normal']))
        
        return elements
    
    def _build_trainee_by_belt_pdf(self, data: dict, styles, title_style) -> list:
        """Build PDF elements for trainee list organized by belt rank."""
        elements = []
        
        # Header
        elements.append(Paragraph("BlackCobra Karate Club", title_style))
        elements.append(Paragraph("Trainee Management Report (By Belt Rank)", styles['Heading2']))
        elements.append(Paragraph(
            f"Generated: {data['generated_date'].strftime('%B %d, %Y')} | "
            f"Status Filter: {data['status_filter']} | Belt Filter: {data['belt_filter']}",
            styles['Normal']
        ))
        elements.append(Spacer(1, 20))
        
        # Summary statistics
        summary_data = [
            ['Metric', 'Count'],
            ['Total Trainees', str(data['total_trainees'])],
            ['Active', str(data['active_trainees'])],
            ['Inactive', str(data['inactive_trainees'])],
            ['Suspended', str(data['suspended_trainees'])],
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc2626')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f3f4f6')),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 20))
        
        # Belt rank order for proper sorting
        belt_order = ['white', 'yellow', 'orange', 'green', 'blue', 'brown', 'black', 'master_degree']
        
        # Trainee list grouped by belt rank
        trainees_by_belt = data.get('trainees_by_belt', {})
        
        if trainees_by_belt:
            elements.append(Paragraph("Trainees by Belt Rank", styles['Heading3']))
            elements.append(Spacer(1, 10))
            
            # Sort belts by defined order
            sorted_belts = sorted(
                trainees_by_belt.keys(),
                key=lambda x: belt_order.index(x.lower().replace(' ', '_')) 
                if x.lower().replace(' ', '_') in belt_order else len(belt_order)
            )
            
            for belt_rank in sorted_belts:
                belt_trainees = trainees_by_belt[belt_rank]
                
                # Belt rank heading
                elements.append(Paragraph(
                    f"{belt_rank.title() if belt_rank != 'master_degree' else 'Master Degree'} Belt ({len(belt_trainees)} trainees)",
                    styles['Heading4']
                ))
                elements.append(Spacer(1, 8))
                
                # Create table for this belt rank
                table_data = [['Name', 'Email', 'Weight Class', 'Age', 'Status', 'Joined']]
                
                for trainee in sorted(belt_trainees, key=lambda x: x['name']):
                    join_date = trainee['join_date'].strftime('%m/%d/%Y') if trainee['join_date'] else 'N/A'
                    table_data.append([
                        trainee['name'],
                        trainee['email'],
                        trainee['weight_class'],
                        str(trainee['age']),
                        trainee['status'],
                        join_date,
                    ])
                
                belt_table = Table(table_data, colWidths=[1.3*inch, 1.4*inch, 1.1*inch, 0.7*inch, 0.9*inch, 0.8*inch])
                belt_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#374151')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('ALIGN', (0, 0), (1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 8),
                    ('FONTSIZE', (0, 1), (-1, -1), 7),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 4),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 4),
                ]))
                elements.append(belt_table)
                elements.append(Spacer(1, 15))
        else:
            elements.append(Paragraph("No trainees found matching the selected filters.", styles['Normal']))
        
        # Footer
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("_" * 80, styles['Normal']))
        elements.append(Paragraph("Authorized By:", styles['Normal']))
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("_" * 40, styles['Normal']))
        elements.append(Paragraph("Admin Signature", styles['Normal']))
        
        return elements
    
    def _build_trainee_list_csv(self, output: io.StringIO, data: dict) -> None:
        """Build CSV content for trainee list report."""
        export_format = data.get('export_format', 'by_user')
        
        if export_format == 'by_belt':
            self._build_trainee_by_belt_csv(output, data)
        else:
            self._build_trainee_by_user_csv(output, data)
    
    def _build_trainee_by_user_csv(self, output: io.StringIO, data: dict) -> None:
        """Build CSV content for trainee list organized by user."""
        writer = csv.writer(output)
        
        # Header
        writer.writerow(['BlackCobra Karate Club - Trainee Management Report'])
        writer.writerow([f"Generated: {data['generated_date'].strftime('%B %d, %Y')}"])
        writer.writerow([f"Status Filter: {data['status_filter']} | Belt Filter: {data['belt_filter']}"])
        writer.writerow([])
        
        # Summary
        writer.writerow(['Summary'])
        writer.writerow(['Metric', 'Count'])
        writer.writerow(['Total Trainees', data['total_trainees']])
        writer.writerow(['Active', data['active_trainees']])
        writer.writerow(['Inactive', data['inactive_trainees']])
        writer.writerow(['Suspended', data['suspended_trainees']])
        writer.writerow([])
        
        # Detailed list
        writer.writerow(['Trainee Details (By User)'])
        writer.writerow(['Name', 'Email', 'Belt Rank', 'Weight Class', 'Age', 'Status', 'Joined'])
        for trainee in data['trainees']:
            join_date = trainee['join_date'].strftime('%m/%d/%Y') if trainee['join_date'] else 'N/A'
            writer.writerow([
                trainee['name'],
                trainee['email'],
                trainee['belt_rank'],
                trainee['weight_class'],
                str(trainee['age']),
                trainee['status'],
                join_date,
            ])
    
    def _build_trainee_by_belt_csv(self, output: io.StringIO, data: dict) -> None:
        """Build CSV content for trainee list organized by belt rank."""
        writer = csv.writer(output)
        
        # Header
        writer.writerow(['BlackCobra Karate Club - Trainee Management Report (By Belt Rank)'])
        writer.writerow([f"Generated: {data['generated_date'].strftime('%B %d, %Y')}"])
        writer.writerow([f"Status Filter: {data['status_filter']} | Belt Filter: {data['belt_filter']}"])
        writer.writerow([])
        
        # Summary
        writer.writerow(['Summary'])
        writer.writerow(['Metric', 'Count'])
        writer.writerow(['Total Trainees', data['total_trainees']])
        writer.writerow(['Active', data['active_trainees']])
        writer.writerow(['Inactive', data['inactive_trainees']])
        writer.writerow(['Suspended', data['suspended_trainees']])
        writer.writerow([])
        
        # Belt rank order for proper sorting
        belt_order = ['white', 'yellow', 'orange', 'green', 'blue', 'brown', 'black', 'master_degree']
        trainees_by_belt = data.get('trainees_by_belt', {})
        
        # Sort belts by defined order
        sorted_belts = sorted(
            trainees_by_belt.keys(),
            key=lambda x: belt_order.index(x.lower().replace(' ', '_')) 
            if x.lower().replace(' ', '_') in belt_order else len(belt_order)
        )
        
        # Group by belt rank
        for belt_rank in sorted_belts:
            belt_trainees = trainees_by_belt[belt_rank]
            
            # Belt rank heading
            belt_label = belt_rank.title() if belt_rank != 'master_degree' else 'Master Degree'
            writer.writerow([f"{belt_label} Belt ({len(belt_trainees)} trainees)"])
            writer.writerow(['Name', 'Email', 'Weight Class', 'Age', 'Status', 'Joined'])
            
            for trainee in sorted(belt_trainees, key=lambda x: x['name']):
                join_date = trainee['join_date'].strftime('%m/%d/%Y') if trainee['join_date'] else 'N/A'
                writer.writerow([
                    trainee['name'],
                    trainee['email'],
                    trainee['weight_class'],
                    str(trainee['age']),
                    trainee['status'],
                    join_date,
                ])
            
            writer.writerow([])  # Empty row between belt groups

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
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer


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

        # Members by belt rank
        members_by_belt = list(
            all_trainees.values('belt_rank')
            .annotate(count=Count('id'))
            .order_by('belt_rank')
        )
        
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
            - participants_by_belt: Breakdown by belt rank
            - participants_by_weight_class: Breakdown by weight class
            - matches_summary: Match statistics
        """
        from core.models import Event, EventRegistration, Match, MatchResult
        
        event = Event.objects.get(id=event_id)
        
        # Get registrations
        registrations = EventRegistration.objects.filter(
            event=event,
            status='registered'
        ).select_related('trainee')
        
        total_registrations = registrations.count()
        
        # Participants by belt rank
        participants_by_belt = list(
            registrations.values('trainee__belt_rank')
            .annotate(count=Count('id'))
            .order_by('trainee__belt_rank')
        )
        
        # Participants by weight class
        participants_by_weight_class = list(
            registrations.values('trainee__weight_class')
            .annotate(count=Count('id'))
            .order_by('trainee__weight_class')
        )
        
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
            'participants_by_belt': participants_by_belt,
            'participants_by_weight_class': participants_by_weight_class,
            'matches_summary': {
                'total': total_matches,
                'completed': completed_matches,
                'scheduled': scheduled_matches,
            },
        }

    
    def export_pdf(self, report_data: Dict[str, Any], report_type: str) -> bytes:
        """
        Export report as PDF.
        Requirements: 7.3
        
        Args:
            report_data: The report data dictionary
            report_type: Type of report ('membership', 'financial', 'event')
            
        Returns:
            PDF file as bytes
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []
        
        # Title style
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
        )
        
        if report_type == 'membership':
            elements = self._build_membership_pdf(report_data, styles, title_style)
        elif report_type == 'financial':
            elements = self._build_financial_pdf(report_data, styles, title_style)
        elif report_type == 'event':
            elements = self._build_event_pdf(report_data, styles, title_style)
        
        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
    
    def _build_membership_pdf(self, data: dict, styles, title_style) -> list:
        """Build PDF elements for membership report."""
        elements = []
        
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
        
        # Belt rank breakdown
        if data['members_by_belt']:
            elements.append(Paragraph("Members by Belt Rank", styles['Heading2']))
            belt_data = [['Belt Rank', 'Count']]
            for item in data['members_by_belt']:
                belt_data.append([item['belt_rank'].title(), str(item['count'])])
            
            belt_table = Table(belt_data, colWidths=[3*inch, 2*inch])
            belt_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(belt_table)
        
        return elements
    
    def _build_financial_pdf(self, data: dict, styles, title_style) -> list:
        """Build PDF elements for financial report."""
        elements = []
        
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
        
        return elements
    
    def _build_event_pdf(self, data: dict, styles, title_style) -> list:
        """Build PDF elements for event report."""
        elements = []
        
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
            belt_data = [['Belt Rank', 'Count']]
            for item in data['participants_by_belt']:
                belt_data.append([
                    item['trainee__belt_rank'].title() if item['trainee__belt_rank'] else 'Unknown',
                    str(item['count'])
                ])
            
            belt_table = Table(belt_data, colWidths=[3*inch, 2*inch])
            belt_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(belt_table)
        
        return elements

    
    def export_csv(self, report_data: Dict[str, Any], report_type: str) -> str:
        """
        Export report as CSV.
        Requirements: 7.3
        
        Args:
            report_data: The report data dictionary
            report_type: Type of report ('membership', 'financial', 'event')
            
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
        
        # Belt breakdown
        writer.writerow(['Members by Belt Rank'])
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
        writer.writerow(['Belt Rank', 'Count'])
        for item in data['participants_by_belt']:
            belt = item['trainee__belt_rank'].title() if item['trainee__belt_rank'] else 'Unknown'
            writer.writerow([belt, item['count']])
        writer.writerow([])
        
        # Participants by weight class
        writer.writerow(['Participants by Weight Class'])
        writer.writerow(['Weight Class', 'Count'])
        for item in data['participants_by_weight_class']:
            writer.writerow([item['trainee__weight_class'], item['count']])

# Participants list section - insert this after line 3105 (story.append(events_table))

    # Participants list
    if include_participants:
        story.append(PageBreak())
        story.append(Paragraph("Event Participants", section_style))
        
        for event in events[:5]:  # Limit to first 5 events per page
            registrations = event.registrations.filter(status='registered')
            if registrations.exists():
                story.append(Paragraph(f"<b>{event.name}</b>", styles['Normal']))
                
                participant_data = [['Participant Name', 'Belt Rank', 'Weight Class']]
                for reg in registrations:
                    trainee = reg.trainee
                    participant_data.append([
                        trainee.profile.user.get_full_name(),
                        trainee.get_belt_rank_display(),
                        trainee.weight_class,
                    ])
                
                participant_table = Table(participant_data, colWidths=[2.5*inch, 1.5*inch, 1.8*inch])
                participant_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ff6b35')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('FONTSIZE', (0, 0), (-1, -1), 7),
                    ('PADDING', (0, 0), (-1, -1), 4),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ]))
                
                story.append(participant_table)
                story.append(Spacer(1, 0.1 * inch))
    
    # Signature section at the end
    story.append(PageBreak())
    story.append(Spacer(1, 0.5 * inch))
    
    signature_style = ParagraphStyle(
        'SignatureStyle',
        parent=styles['Normal'],
        fontSize=9,
        fontName='Helvetica',
        alignment=TA_LEFT,
    )
    
    # Signature table layout
    sig_data = [
        ['', ''],
        ['_' * 35, '_' * 35],
        ['Name: ' + current_user, 'Date: ' + datetime.now().strftime('%B %d, %Y')],
        ['', ''],
        ['Prepared by:', ''],
    ]
    
    sig_table = Table(sig_data, colWidths=[2.9*inch, 2.9*inch])
    sig_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(sig_table)
    
    # Build PDF
    doc.build(story)
    return response

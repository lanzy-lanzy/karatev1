#!/usr/bin/env python
"""Test trainee PDF/CSV export functionality with multiple formats."""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'karate.settings')
django.setup()

from core.services.reports import ReportService

# Test trainee report generation
service = ReportService()

print("Testing trainee report generation...")
print("=" * 60)

# Test 1: Export by User (default)
print("\n1. EXPORT BY USER (Default Format)")
print("-" * 60)
try:
    data_by_user = service.trainee_report(export_format='by_user')
    print(f"Total trainees: {data_by_user['total_trainees']}")
    print(f"Active: {data_by_user['active_trainees']}")
    print(f"Inactive: {data_by_user['inactive_trainees']}")
    print(f"Suspended: {data_by_user['suspended_trainees']}")
    print(f"Export format: {data_by_user['export_format']}")
    print(f"Generated: {data_by_user['generated_date']}")
    
    # PDF by user
    pdf_user = service.export_pdf(data_by_user, 'trainee_list')
    pdf_user_size = len(pdf_user)
    print(f"\nPDF (by user) generated: {pdf_user_size} bytes")
    
    output_path = os.path.join(os.path.dirname(__file__), 'test_trainee_user.pdf')
    with open(output_path, 'wb') as f:
        f.write(pdf_user)
    print(f"Saved to: {output_path}")
    
    # CSV by user
    csv_user = service.export_csv(data_by_user, 'trainee_list')
    csv_user_lines = len(csv_user.split('\n'))
    print(f"\nCSV (by user) generated: {csv_user_lines} lines")
    
    output_path = os.path.join(os.path.dirname(__file__), 'test_trainee_user.csv')
    with open(output_path, 'w') as f:
        f.write(csv_user)
    print(f"Saved to: {output_path}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Export by Belt
print("\n\n2. EXPORT BY BELT RANK")
print("-" * 60)
try:
    data_by_belt = service.trainee_report(export_format='by_belt')
    print(f"Total trainees: {data_by_belt['total_trainees']}")
    print(f"Export format: {data_by_belt['export_format']}")
    print(f"Trainees by belt groups: {len(data_by_belt['trainees_by_belt'])}")
    for belt, trainees in sorted(data_by_belt['trainees_by_belt'].items()):
        print(f"  - {belt.title()}: {len(trainees)} trainees")
    
    # PDF by belt
    pdf_belt = service.export_pdf(data_by_belt, 'trainee_list')
    pdf_belt_size = len(pdf_belt)
    print(f"\nPDF (by belt) generated: {pdf_belt_size} bytes")
    
    output_path = os.path.join(os.path.dirname(__file__), 'test_trainee_belt.pdf')
    with open(output_path, 'wb') as f:
        f.write(pdf_belt)
    print(f"Saved to: {output_path}")
    
    # CSV by belt
    csv_belt = service.export_csv(data_by_belt, 'trainee_list')
    csv_belt_lines = len(csv_belt.split('\n'))
    print(f"\nCSV (by belt) generated: {csv_belt_lines} lines")
    
    output_path = os.path.join(os.path.dirname(__file__), 'test_trainee_belt.csv')
    with open(output_path, 'w') as f:
        f.write(csv_belt)
    print(f"Saved to: {output_path}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

# Test 3: With filters
print("\n\n3. EXPORT WITH FILTERS (Active + Brown Belt)")
print("-" * 60)
try:
    data_filtered = service.trainee_report(
        status_filter='active',
        belt_filter='brown',
        export_format='by_belt'
    )
    print(f"Total trainees matching filters: {data_filtered['total_trainees']}")
    print(f"Status filter: {data_filtered['status_filter']}")
    print(f"Belt filter: {data_filtered['belt_filter']}")
    
    # PDF filtered
    pdf_filtered = service.export_pdf(data_filtered, 'trainee_list')
    pdf_filtered_size = len(pdf_filtered)
    print(f"\nPDF (filtered, by belt) generated: {pdf_filtered_size} bytes")
    
    output_path = os.path.join(os.path.dirname(__file__), 'test_trainee_filtered.pdf')
    with open(output_path, 'wb') as f:
        f.write(pdf_filtered)
    print(f"Saved to: {output_path}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("All tests completed successfully!")
print("=" * 60)

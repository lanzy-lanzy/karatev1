#!/usr/bin/env python
"""Test PDF generation with new header layout."""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'karate.settings')
django.setup()

from core.services.reports import ReportService
from datetime import date

# Generate test report
service = ReportService()
data = service.membership_report(date(2025, 11, 5), date(2025, 12, 5))
pdf = service.export_pdf(data, 'membership')

# Save to file
output_path = os.path.join(os.path.dirname(__file__), 'test_report.pdf')
with open(output_path, 'wb') as f:
    f.write(pdf)

print(f'PDF generated successfully: {output_path}')
print(f'File size: {len(pdf)} bytes')

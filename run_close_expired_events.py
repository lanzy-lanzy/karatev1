#!/usr/bin/env python
"""
Script to run the close_expired_events management command.
This should be scheduled to run daily via cron or a task scheduler.

Usage:
    python run_close_expired_events.py
    
Or schedule with cron:
    0 0 * * * cd /path/to/karate && python manage.py close_expired_events
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'karate.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.core.management import call_command

if __name__ == '__main__':
    print("Running close_expired_events management command...")
    try:
        call_command('close_expired_events')
        print("Command completed successfully.")
    except Exception as e:
        print(f"Error running command: {e}")
        sys.exit(1)

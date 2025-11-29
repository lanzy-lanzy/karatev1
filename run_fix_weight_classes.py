#!/usr/bin/env python
"""
Script to run the fix_weight_classes management command directly.
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'karate.settings')
sys.path.insert(0, os.path.dirname(__file__))

django.setup()

# Now import and run the command
from django.core.management import call_command

if __name__ == '__main__':
    call_command('fix_weight_classes')

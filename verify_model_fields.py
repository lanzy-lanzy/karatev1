import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'karate.settings')
django.setup()

from core.models import Registration
print("Fields:", [f.name for f in Registration._meta.get_fields()])

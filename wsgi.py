"""
WSGI config for aisite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.core.management import call_command
from django.db.utils import OperationalError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aisite.settings')

application = get_wsgi_application()

# Try to run migrations at startup, handle failure gracefully
try:
    call_command('migrate', noinput=True)
except OperationalError:
    print("Migrations failed to apply. Check your database settings.")
except Exception as e:
    print(f'An error occurred: {e}')

"""
WSGI config for counter_automation project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

# Get environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'counter_automation.settings')

application = get_wsgi_application()

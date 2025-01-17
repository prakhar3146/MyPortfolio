"""
WSGI config for MyPortfolio project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
#Modified for render on 17-01-2025
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyPortfolio.MyPortfolio.settings')

application = get_wsgi_application()

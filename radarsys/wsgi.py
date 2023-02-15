"""
WSGI config for radarsys project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from .socketconfig import sio
import socketio

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "radarsys.settings")

application = get_wsgi_application()
application = socketio.WSGIApp(sio, application)

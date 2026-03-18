import os
from django.core.wsgi import get_wsgi_application

# Set default settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# WSGI application
application = get_wsgi_application()

"""
WSGI config for stuff4friends project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stuff4friends.settings")

application = get_wsgi_application()

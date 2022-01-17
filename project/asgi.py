import os
from django.core.asgi import get_asgi_application
from apps.auth2 import routing as user_ws_routes

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project")

application = get_asgi_application()

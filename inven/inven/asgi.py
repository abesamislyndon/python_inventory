# import os
# from django.core.asgi import get_asgi_application

# # Set the default Django settings module for the 'asgi' application.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inven.settings')

# # Get the ASGI application
# application = get_asgi_application()
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from app.clients.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inven.settings")
django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)
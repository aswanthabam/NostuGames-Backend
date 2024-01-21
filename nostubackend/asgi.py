import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import django
from mysockets.auth import RoomAuthMiddleware
from .routing import ws_patterns
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nostubackend.settings')
django.setup()

app = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket":RoomAuthMiddleware(URLRouter(ws_patterns)),
})
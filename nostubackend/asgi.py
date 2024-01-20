import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from mysockets.consumer import DataAccessor
from django.urls import path
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nostubackend.settings')
django.setup()

ws_patterns = [
    path('ws/user/access/', DataAccessor.as_asgi())
]

app = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket":URLRouter(ws_patterns),
})
import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from mysockets.consumer import DataAccessor
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nostubackend.settings')

application = get_asgi_application()
ws_patterns = [
    path('ws/user/access/', DataAccessor.as_asgi())
]

app = ProtocolTypeRouter({
    "http": application,
    "websocket":URLRouter(ws_patterns),
})
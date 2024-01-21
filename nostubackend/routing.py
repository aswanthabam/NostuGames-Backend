from mysockets.consumer import BingoGame
from django.urls import path

ws_patterns = [
    path('ws/game/bingo/', BingoGame.as_asgi())
]
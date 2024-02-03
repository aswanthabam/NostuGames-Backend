from django.urls import path, include
from .views import GameInfoAPI
urlpatterns = [
    path('info/',GameInfoAPI.as_view())
]

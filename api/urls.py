from django.urls import path, include

urlpatterns = [
    path('game/',include('api.game.urls'))
]

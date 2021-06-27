from django.urls import path

from game.api import CharacterAPI, SessionAPI, PlayerAPI

urlpatterns = [
    path("api/characters/", CharacterAPI.as_view()),
    path("api/session/", SessionAPI.as_view()),
    path("api/player/", PlayerAPI.as_view()),
]
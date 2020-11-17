from django.urls import path

from game.api import CharacterAPI, GameAPI

urlpatterns = [
    path("api/characters/", CharacterAPI.as_view()),
    path("api/game/", GameAPI.as_view()),
]
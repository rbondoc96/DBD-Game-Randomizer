from django.urls import path

from game.api import CharacterAPI

urlpatterns = [
    path("api/characters/", CharacterAPI.as_view()),
]
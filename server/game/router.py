from rest_framework import routers

from game.api import CharacterAPI

router = routers.DefaultRouter()
router.register(r"characters", CharacterAPI, basename="characters")
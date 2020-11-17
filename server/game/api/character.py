from rest_framework.views import APIView
from rest_framework.response import Response

import os
import base64

from server.permissions import ReadOnly

from game.models import Character
from game.serializers import CharacterSerializer

class CharacterAPI(APIView):
    permission_classes = [ReadOnly]

    def get(self, request, *args, **kwargs):
        characters = Character.objects.all()
        return Response(characters)

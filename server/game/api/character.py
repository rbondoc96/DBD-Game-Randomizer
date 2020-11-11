from rest_framework.views import APIView
from rest_framework.response import Response

from server.permissions import ReadOnly

from game.models import Character
from game.serializers import CharacterSerializer

class CharacterAPI(APIView):
    permission_classes = [ReadOnly]

    def get(self, request, *args, **kwargs):
        characters = Character.objects.all()
        serializer = CharacterSerializer(characters, many=True)
        return Response(serializer.data)

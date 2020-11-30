from random import sample, randint

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from game.models import(
    Player,
)
from game.serializers import(
    PlayerCreateSerializer,
)

from game.utils import generate_random_player

def randomize_player(player, role, no_licensed_chars=False):
    random_player = generate_random_player(
       role, 
       no_licensed_chars=no_licensed_chars
    )
    random_data = PlayerCreateSerializer(random_player).data

    del random_data["id"]
    del random_data["player_id"]
    random_player.delete()

    serializer = PlayerCreateSerializer(
        player, 
        data=random_data,     
        partial=True,
    )

    if serializer.is_valid():
        print("Successfully randomized player")
        return serializer.save()
    else:
        print("Randomization unsuccessful")    
        return player        

class PlayerAPI(APIView):

    def get(self, request, *args, **kwargs):
        params = request.query_params
        action = params.get("action")
        
        player_id = params.get("playerId")
        player_role = params.get("playerRole")
        no_licensed_chars = bool(params.get("noLicensedChars"))

        if action == "randomize":
            player = Player.objects.get(player_id=player_id)
            player = randomize_player(
                player, 
                player_role, 
                no_licensed_chars=no_licensed_chars
            )

            return Response({
                "message": "Player successfully randomized."
            }, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        params = request.query_params
        player_id = params.get("playerId")

        try:
            player = Player.objects.get(player_id=player_id)
            player.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Player.DoesNotExist:
            return Response({
                "error": "Player does not exist",
            },status=status.HTTP_400_BAD_REQUEST)
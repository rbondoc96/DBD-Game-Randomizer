from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from game.models import Player
from game.serializers import PlayerSerializer

from game.utils.logs import Logger
from game.utils.player import PlayerUtils

TAG = "PlayerAPI"
logger = Logger(TAG)

class PlayerAPI(APIView):

    def get(self, request, *args, **kwargs):
        player = PlayerUtils.get_client_player(request)

        params = request.query_params
        action = params.get("action")
        role = params.get("role")
        name = params.get("name")
        block_list = params.get("blockList")
        no_licensed_chars = params.get("noLicensedChars")

        if no_licensed_chars is not None:
            no_licensed_chars = no_licensed_chars.lower() == "true"
        else:
            no_licensed_chars = False

        if action == "randomize":
            if role is not None:
                player = PlayerUtils.randomize(
                    player,
                    role,
                    no_licensed_chars=no_licensed_chars
                )       
            else:
                player = PlayerUtils.randomize(
                    player,
                    player.role,
                    no_licensed_chars=no_licensed_chars
                )

        elif action == "rename" and name is not None:
            if len(name) <= 255:
                player.name = name.strip()
                player.save()
            else:
                err = ErrorResponse(
                    ErrorTypes.PlayerNameTooLong.code,
                    "Please choose a name with 255 characters or less."
                )
                return Response(
                    err.message(),
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        elif action == "block" and block_list is not None:
            pass

        return Response(
            PlayerUtils.to_dict(player),            
            status=status.HTTP_200_OK
        )

from rest_framework.views import APIView
from rest_framework.response import Response

import os
from random import randint

from server.permissions import ReadOnly

from game.models import Perk, Character
from game.serializers import PerkSerializer, CharacterSerializer

class GameAPI(APIView):
    permission_classes = [ReadOnly]

    def get(self, request, *args, **kwargs):
        params = request.query_params
        game_type = params.get("gameType")
        num_players = int(params.get("numPlayers"))

        if num_players <= 0 or (num_players > 5 and game_type != "custom"):
            return Response({
                "error": "Number of Players must be between 1 and 5."
            })

        payload = {}
        if game_type == "killer":
            if num_players > 1:
                return Response({
                    "error": "There can only be 1 Killer."
                })

            killers = Character.objects.filter(type="Killer")
            choice_idx = randint(0, len(killers)-1)
            choice = killers[choice_idx]
            
            perks = Perk.objects.filter(type="Killer", tier=3)
            
            perk_choices = []
            for _ in range(0, len(perks)):
                idx = randint(0, len(perks)-1)
                perk_choices.append(perks[idx])

            killer = CharacterSerializer(choice)

            perk_serializer = PerkSerializer(
                perk_choices,
                many=True,
            )

            payload = {
                "killer": killer.data,
                "killerPerks": perk_serializer.data,
            }
        
        elif game_type == "survivor":
            if num_players > 4:
                return Response({
                    "error": "Number of Survivors must be between 1 and 4."
                })
            
            survivors = Character.objects.filter(type="Survivor")
            perks = Perk.objects.filter(type="Survivor", tier=3)
            payload = {}

            for i in range(0, num_players):
                idx = randint(0, len(survivors)-1)
                survivor = CharacterSerializer(survivors[idx])
                payload[f"survivor{i+1}"] = {
                    "survivor": survivor.data,
                }
        
        elif game_type == "custom":
            killers = Character.objects.filter(type="Killer")
            choice_idx = randint(0, len(killers)-1)
            choice = killers[choice_idx]
            
            perks = Perk.objects.filter(type="Killer", tier=3)
            
            perk_choices = []
            for _ in range(0, len(perks)):
                idx = randint(0, len(perks)-1)
                perk_choices.append(perks[idx])

            killer = CharacterSerializer(choice)

            perk_serializer = PerkSerializer(
                perk_choices,
                many=True,
            )

            payload["killer"] = {
                "killer": killer.data,
                "killerPerks": perk_serializer.data,
            }
            
            survivors = Character.objects.filter(type="Survivor")
            perks = Perk.objects.filter(type="Survivor", tier=3)

            payload["survivors"] = {}
            for i in range(0, num_players-1):
                idx = randint(0, len(survivors)-1)
                survivor = CharacterSerializer(survivors[idx])
                payload["survivors"][f"survivor{i+1}"] = {
                    "survivor": survivor.data,
                }

        else:
            return Response({})
        
        return Response({
            "mode": game_type.capitalize(),
            "game": payload,
        })
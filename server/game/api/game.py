from rest_framework.views import APIView
from rest_framework.response import Response

import os
from random import randint, sample

from server.permissions import ReadOnly

# from game.models import Perk, Character, Item, Offering
from game.serializers import (
    OfferingSerializer,
    ItemSerializer,
    PerkSerializer, 
    CharacterSerializer
)

class GameAPI(APIView):
    permission_classes = [ReadOnly]

    def get(self, request, *args, **kwargs):
        params = request.query_params
        game_type = params.get("gameType")
        num_players = int(params.get("numPlayers"))
        no_licensed_characters = bool(params.get("nonLicensedOnly"))

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

            if no_licensed_characters:
                killers = Character.objects.filter(
                    type="Killer"
                ).exclude(
                    is_licensed=True
                )
            else:
                killers = Character.objects.filter(type="Killer")
            choice_idx = randint(0, len(killers)-1)
            choice = killers[choice_idx]
            
            perks = Perk.objects.filter(type="Killer", tier=3)
            offerings = Offering.objects.exclude(type="Survivor")
            perk_choices = [perks[unique_idx] 
                    for unique_idx in sample(range(0, len(perks)), 4)
                ]                
            offering = offerings[sample(range(0, len(offerings)), 1)[0]]

            killer = CharacterSerializer(choice)

            p_serializer = PerkSerializer(
                perk_choices,
                many=True,
            )
            o_serializer = OfferingSerializer(offering)

            payload["killer"] = {
               **killer.data,
                "perks": p_serializer.data,
                "offering": o_serializer.data,
            }
        
        elif game_type == "survivor":
            if num_players > 4:
                return Response({
                    "error": "Number of Survivors must be between 1 and 4."
                })
            
            payload["survivors"] = []
            
            if no_licensed_characters:
                survivors = Character.objects.filter(
                    type="Survivor"
                ).exclude(
                    is_licensed=True
                )
            else:
                survivors = Character.objects.filter(type="Survivor")
            perks = Perk.objects.filter(type="Survivor", tier=3)
            items = Item.objects.all()
            offerings = Offering.objects.exclude(type="Killer")

            for _ in range(0, num_players):
                idx = randint(0, len(survivors)-1)
                survivor = CharacterSerializer(survivors[idx])
                
                perk_choices = [perks[unique_idx] 
                    for unique_idx in sample(range(0, len(perks)), 4)
                ]

                item = items[sample(range(0, len(items)), 1)[0]]
                offering = offerings[sample(range(0, len(offerings)), 1)[0]]

                i_serializer = ItemSerializer(item)
                o_serializer = OfferingSerializer(offering)
                p_serializer = PerkSerializer(perk_choices, many=True)
                
                payload["survivors"].append({
                    **survivor.data,
                    "perks": p_serializer.data,
                    "item": i_serializer.data,
                    "offering": o_serializer.data,
                })
        
        elif game_type == "custom":
            killers = Character.objects.filter(type="Killer")
            choice_idx = randint(0, len(killers)-1)
            choice = killers[choice_idx]
            
            perks = Perk.objects.filter(type="Killer", tier=3)
            perk_choices = [perks[unique_idx] 
                    for unique_idx in sample(range(0, len(perks)), 4)
                ]
            offerings = Offering.objects.exclude(type="Survivor")
            offering = offerings[sample(range(0, len(offerings)), 1)[0]]

            killer = CharacterSerializer(choice)

            p_serializer = PerkSerializer(
                perk_choices,
                many=True,
            )
            o_serializer = OfferingSerializer(offering)

            payload["killer"] = {
               **killer.data,
                "perks": p_serializer.data,
                "offering": o_serializer.data,
            }
            
            survivors = Character.objects.filter(type="Survivor")
            perks = Perk.objects.filter(type="Survivor", tier=3)
            items = Item.objects.all()
            offerings = Offering.objects.exclude(type="Killer")

            payload["survivors"] = []
            for i in range(0, num_players-1):
                idx = randint(0, len(survivors)-1)
                survivor = CharacterSerializer(survivors[idx])

                perk_choices = [perks[unique_idx] 
                    for unique_idx in sample(range(0, len(perks)), 4)
                ]

                item = items[sample(range(0, len(items)), 1)[0]]
                offering = offerings[sample(range(0, len(offerings)), 1)[0]]

                i_serializer = ItemSerializer(item)
                o_serializer = OfferingSerializer(offering)
                p_serializer = PerkSerializer(perk_choices, many=True)
                
                payload["survivors"].append({
                    **survivor.data,
                    "perks": p_serializer.data,
                    "item": i_serializer.data,
                    "offering": o_serializer.data,
                })
        else:
            return Response({})
        
        return Response({
            "game": {
                "mode": game_type.capitalize(),
                "meta": {
                    "map": "???",
                    "obsession": "???",
                    "hatchLocation": "???",
                },
                "players": payload,
            },
        })
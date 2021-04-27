import json
from random import randint, choice as random_choice

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from game.utils.logs import Logger

# Importing module to avoid ImportError
import game.models as models
from game.serializers import(
    PlayerSerializer,
    PlayerCreateSerializer,
)

from game.utils.random import get_random_index

TAG = "PlayerAPI"
logger = Logger(TAG)

def randomize_player(instance, role, no_licensed_chars=False):
    # Auto Survivor assignment may avoid issue with 2+ Killers in a session
    if(role is None):
        role = "Survivor"

    role__proper = role.title()
    
    instance.role = role__proper

    # Get random Character based off role and restrictions
    characters = models.Character.objects.filter(type=role__proper)
    if no_licensed_chars:
        characters = characters.exclude(is_licensed=True)
    
    character = random_choice(characters)
    instance.character = character

    # Get random Player offering
    offering = None
    if randint(0,3):
        if role.lower() == "survivor":
            offerings = models.Offering.objects.exclude(type="Killer")
        else:
            offerings = models.Offering.objects.exclude(type="Survivor")

        offering = random_choice(offerings)
        instance.offering = offering

    
    # Get random Player resource (Item or Power)
    # Must reset Player resource from previous randomization
    instance.item = None;
    instance.power = None;
    if role.lower() == "survivor":
        items = models.Item.objects.all()
        item = random_choice(items)
        instance.item = item
    else:
        instance.power = instance.character.power

    # Get random add-ons
    # Must reset resource addons
    instance.item_addons.clear()
    instance.power_addons.clear()
    if instance.item is not None:
        addon_set = models.ItemAddOn.objects.filter(
            type=instance.item.type
        )

        for _ in range(0, 2):    
            if len(addon_set) > 0:
                addon = random_choice(addon_set)
                instance.item_addons.add(addon)
            else:
                addon = None

            print("Addon:", addon)

    else:
        addon_set = models.PowerAddOn.objects.filter(
            power=instance.power
        )
        
        for _ in range(0, 2):
            if len(addon_set) == 1:
                addon = addon_set[0]
                instance.power_addons.add(addon)
            else:
                addon = None

            print("Addon", addon)        


    perk_set = models.Perk.objects.filter(type=role__proper)
    instance.perks.clear()
    
    while instance.perks.count() < 4:
        perk = random_choice(perk_set)

        if (perk in instance.perks.all()) and \
            (perk_set.count() > 4):
            while perk in instance.perks.all():
                perk = random_choice(perk_set)
                    
        instance.perks.add(perk)
        
    instance.save()
    return instance

class PlayerAPI(APIView):

    def get(self, request, *args, **kwargs):
        player = request.session.get("player")

        # Get existing player if there is one, otherwise, create a new player
        if player is None:
            player = models.Player.objects.create()
            data = PlayerSerializer(player).data          
            
            # Must be a dict, not model object
            request.session["player"] = data
        
        else:
            id = player.get("player_id")
            try:
                player = models.Player.objects.get(player_id=id)
            except models.Player.DoesNotExist:
                player = models.Player.objects.create()
                data = PlayerSerializer(player).data          
                
                request.session["player"] = data
        
        params = request.query_params
        action = params.get("action")
        role = params.get("role")
        name = params.get("name")
        no_licensed_chars = params.get("noLicensedChars")

        if no_licensed_chars is not None:
            no_licensed_chars = True \
                if params.get("noLicensedChars").lower() == "true" else False

        if action == "randomize":
            if role is not None and no_licensed_chars is not None:
                player = randomize_player(
                    player, 
                    role,
                    no_licensed_chars=no_licensed_chars
                )
            elif role is not None and no_licensed_chars is None:
                player = randomize_player(
                    player, 
                    role,
                )        
            elif role is None and no_licensed_chars is not None:
                player = randomize_player(
                    player, 
                    player.role,
                    no_licensed_chars=no_licensed_chars
                ) 
            else:
                player = randomize_player(
                    player, 
                    player.role,
                ) 

        elif action == "rename" and name is not None:
            if len(name) <= 255:
                player.name = name.strip()
                player.save()
            else:
                return Response({
                    "error": "Name is longer than 255 characters."
                }, status=status.HTTP_400_BAD_REQUEST)
        
        payload = PlayerSerializer(player).data
        return Response({
            "player": payload
        }, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        params = request.query_params
        player_id = params.get("playerId")

        try:
            player = models.Player.objects.get(player_id=player_id)
            player.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Player.DoesNotExist:
            return Response({
                "error": "Player does not exist",
            },status=status.HTTP_400_BAD_REQUEST)
from rest_framework import status
from rest_framework.response import Response

from random import sample, randint, choice as random_choice

from game.utils.error import ErrorResponse, ErrorTypes
from game.utils.error.exceptions import PlayerImproperlyConfigured
from game.serializers import PlayerSerializer
from game.models import(
    Player,
    Character,
    Offering,
    Perk,
    Item, Power,
    ItemAddOn, PowerAddOn,
)

class PlayerUtils:

    @staticmethod
    def set_client_player(request, player):
        """
            Set the client session's Player
        """
        request.session["player"] = PlayerSerializer(player).data


    @staticmethod
    def new_client_player(request):
        """ 
            Return a new Player instance and set as the current client 
            session's Player
        """
        player = PlayerUtils.generate("Survivor")
        PlayerUtils.set_client_player(request, player)
        
        return player


    @staticmethod
    def get_client_player(request):
        """ 
            Get the client session's Player, or return a new one 
        """
        player = None
        player_dict = request.session.get("player")

        if player_dict is None:
            player = PlayerUtils.new_client_player(request)
        
        else:
            pid = player_dict.get("player_id")

            if pid is not None:
                try:
                    player = Player.objects.get(player_id=pid)

                except Player.DoesNotExist:
                    player = PlayerUtils.new_client_player(request)

            else:
                player = PlayerUtils.new_client_player(request)

        return player    


    @staticmethod
    def reset(instance):
        instance.item = None
        instance.power = None
        instance.item_addons.clear()
        instance.power_addons.clear()
        instance.perks.clear()

        instance.save()
        return instance


    @staticmethod
    def to_dict(instance):
        data = PlayerSerializer(instance).data

        return {
            "player": data
        }


    @staticmethod
    def randomize_character(instance, is_licensed):
        print("Role " + str(instance.role))

        characters = Character.objects.filter(type=instance.role)
        if is_licensed:
            characters = characters.exclude(is_licensed=True)  

        character = random_choice(characters)
        instance.character = character

        instance.save()
        return instance


    @staticmethod
    def randomize_resource(instance):
        if instance.character.type.lower() == "survivor":
            instance.item = random_choice(Item.objects.all())
        else:
            try:
                instance.power = Power.objects.get(
                    owner=instance.character
                )
            except Power.DoesNotExist:
                instance.power = None

        instance.save()
        return instance


    @staticmethod
    def randomize_addons(instance):
        if instance.item is not None and instance.role.lower() == "survivor":
            addons = list(ItemAddOn.objects.filter(
                type=instance.item.type
            ))

            for _ in range(0, 2):    
                if len(addons) > 0:
                    addon = random_choice(addons)
                    addons.remove(addon)
                    instance.item_addons.add(addon)

        elif instance.power is not None and instance.role.lower() == "killer":
            addons = list(PowerAddOn.objects.filter(
                power=instance.power
            ))
            
            for _ in range(0, 2):
                if len(addons) > 0:
                    addon = random_choice(addons)
                    addons.remove(addon)
                    instance.power_addons.add(addon)

        instance.save()
        return instance                    


    @staticmethod
    def randomize_offering(instance):
        if instance.character.type.lower() == "survivor":
            offerings = Offering.objects.exclude(type="Killer")
        else:
            offerings = Offering.objects.exclude(type="Survivor")

        instance.offering = random_choice(offerings)
        
        instance.save()
        return instance


    @staticmethod
    def randomize_perks(instance):
        perks = list(Perk.objects.filter(type=instance.role))
        
        while instance.perks.count() < 4 and len(perks) > 0:
            perk = random_choice(perks)
            instance.perks.add(perk)
            perks.remove(perk)

        instance.save()
        return instance


    @staticmethod
    def generate(role, no_licensed_chars=False):
        if role is None:
            role = "Survivor"
        
        role = role.title()
        attributes = {
            "role": role,
        }

        player = Player.objects.create(role=role)
        PlayerUtils.randomize_character(player, no_licensed_chars)
        PlayerUtils.randomize_resource(player)
        PlayerUtils.randomize_addons(player)   
        PlayerUtils.randomize_offering(player)
        PlayerUtils.randomize_perks(player)
        
        player.save()
        return player


    @staticmethod
    def randomize(instance, role, no_licensed_chars=False):
        instance = PlayerUtils.reset(instance)
        instance.role = role.title()

        PlayerUtils.randomize_character(instance, no_licensed_chars)
        PlayerUtils.randomize_resource(instance)
        PlayerUtils.randomize_addons(instance)   
        PlayerUtils.randomize_offering(instance)
        PlayerUtils.randomize_perks(instance)
            
        instance.save()
        return instance


    @staticmethod
    def reverse_role(instance, no_licensed_chars=False):
        role = instance.role.lower()

        if role == "survivor":
            PlayerUtils.randomize(
                instance, 
                "Killer",
                no_licensed_chars=no_licensed_chars
            )

        else:
            PlayerUtils.randomize(
                instance, 
                "Survivor",
                no_licensed_chars=no_licensed_chars
            )

        instance.save()
        return instance
        
    
from rest_framework import serializers

from game.models import Player
from game.serializers import(
    CharacterSerializer,
    EffectSerializer,
    ItemSerializer,
    PerkSerializer,
    OfferingSerializer,
    PowerSerializer,
    ItemAddOnSerializer, PowerAddOnSerializer
)

class PlayerSerializer(serializers.ModelSerializer):
    character = CharacterSerializer()
    item = ItemSerializer()
    power = PowerSerializer()
    offering = OfferingSerializer()
    perks = PerkSerializer(many=True)
    item_addons = ItemAddOnSerializer(many=True)
    power_addons = PowerAddOnSerializer(many=True)
    
    class Meta:
        model = Player
        fields = [
            "id",
            "player_id",
            "name",
            "role",
            "character",
            "item",
            "power",
            "item_addons",
            "power_addons",
            "offering",
            "perks",
            "created",
        ]

class PlayerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = "__all__"    
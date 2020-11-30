from rest_framework import serializers

from game.models import Player
from game.serializers import(
    CharacterSerializer,
    ItemSerializer,
    PerkSerializer,
    OfferingSerializer,
)

class PlayerSerializer(serializers.ModelSerializer):
    character = CharacterSerializer()
    item = ItemSerializer()
    offering = OfferingSerializer()
    perks = PerkSerializer(many=True)
    
    class Meta:
        model = Player
        fields = "__all__"

class PlayerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = "__all__"    
from rest_framework import serializers

from game.models import Perk

from game.serializers import EffectSerializer

class PerkSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    rarity = serializers.StringRelatedField()

    effects = EffectSerializer(many=True)
    
    class Meta:
        model = Perk
        fields = [
            "id",
            "owner",
            "rarity",
            "name",
            "type",
            "tier",
            "description",
            "quote",
            "image",
            "effects",
        ] 
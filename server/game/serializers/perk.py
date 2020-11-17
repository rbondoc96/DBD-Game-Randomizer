from rest_framework import serializers

from game.models import Perk

class PerkSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    rarity = serializers.StringRelatedField()
    
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
from rest_framework import serializers

from game.models import Perk

from game.serializers import EffectSerializer

class PerkSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    rarities  = serializers.StringRelatedField(many=True)
    effects = EffectSerializer(many=True)
    
    class Meta:
        model = Perk
        fields = "__all__"

        # fields = [
        #     "id",
        #     "owner",
        #     "rarity",
        #     "name",
        #     "type",
        #     "tier",
        #     "description",
        #     "quote",
        #     "image",
        #     "effects",
        #     "tiers",
        # ] 
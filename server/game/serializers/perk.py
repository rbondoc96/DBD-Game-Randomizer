from rest_framework import serializers

from game.models import Perk

from game.serializers import EffectSerializer

class PerkSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    rarities  = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Perk

        fields = [
            "id",
            "name",
            "type",            
            "owner",
            "rarities",
            "overlay",
        ] 
from rest_framework import serializers

from game.models import Offering

class OfferingSerializer(serializers.ModelSerializer):
    rarities = serializers.StringRelatedField(many=True)
        
    class Meta:
        model = Offering
        fields = [
            "id",
            "name",
            "type",
            "rarities",
            "overlay",
        ]
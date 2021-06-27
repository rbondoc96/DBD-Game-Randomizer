from rest_framework import serializers

from game.models import Power

from game.serializers import CharacterSerializer

class PowerSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()

    class Meta:
        model = Power
        fields = [
            "id",
            "name",
            "owner",
            "primary_overlay",
            "secondary_overlay",
            "tertiary_overlay",
        ]
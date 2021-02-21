from rest_framework import serializers

from game.models import Power

from game.serializers import CharacterSerializer

class PowerSerializer(serializers.ModelSerializer):
    owner = CharacterSerializer()

    class Meta:
        model = Power
        fields = "__all__"
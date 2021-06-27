from rest_framework import serializers

from game.models import Character

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = [
            "id",
            "name",
            "type",
            "is_licensed",
            "image",
        ]
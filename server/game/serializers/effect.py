from rest_framework import serializers

from game.models import Effect

class EffectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Effect
        fields = "__all__"
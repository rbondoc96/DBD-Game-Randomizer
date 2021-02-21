from rest_framework import serializers

from game.models import Effect, EffectType

from game.serializers import ConditionSerializer

class EffectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EffectType
        fields = "__all__"

class EffectSerializer(serializers.ModelSerializer):
    type = EffectTypeSerializer()
    conditions = ConditionSerializer(many=True)
    
    class Meta:
        model = Effect
        fields = "__all__"
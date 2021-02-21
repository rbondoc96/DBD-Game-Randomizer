from rest_framework import serializers

from game.models import Condition, ConditionType

from game.serializers import EventSerializer

class ConditionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConditionType
        fields = "__all__"

class ConditionSerializer(serializers.ModelSerializer):
    type = ConditionTypeSerializer()
    event = EventSerializer()

    class Meta:
        model = Condition
        fields = "__all__"
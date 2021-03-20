from rest_framework import serializers

from game.models import ItemAddOn, PowerAddOn
from game.serializers import (
    PowerSerializer,
)

class ItemAddOnSerializer(serializers.ModelSerializer):
    type = serializers.StringRelatedField()
    rarities  = serializers.StringRelatedField(many=True)

    class Meta:
        model = ItemAddOn
        fields = "__all__"

class PowerAddOnSerializer(serializers.ModelSerializer):
    power = PowerSerializer()
    rarities  = serializers.StringRelatedField(many=True)

    class Meta:
        model = PowerAddOn
        fields = "__all__"
from rest_framework import serializers

from game.models import ItemAddOn, PowerAddOn
from game.serializers import (
    PowerSerializer,
)

class ItemAddOnSerializer(serializers.ModelSerializer):
    type = serializers.StringRelatedField()
    rarity = serializers.StringRelatedField()

    class Meta:
        model = ItemAddOn
        fields = "__all__"

class PowerAddOnSerializer(serializers.ModelSerializer):
    power = PowerSerializer()
    rarity = serializers.StringRelatedField()

    class Meta:
        model = PowerAddOn
        fields = "__all__"
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
        fields = [
            "id",
            "name",
            "type",
            "rarities",
            "overlay",
        ]

class PowerAddOnSerializer(serializers.ModelSerializer):
    power = serializers.StringRelatedField()
    rarities  = serializers.StringRelatedField(many=True)

    class Meta:
        model = PowerAddOn
        fields = [
            "id",
            "name",
            "power",
            "rarities",
            "overlay"
        ]
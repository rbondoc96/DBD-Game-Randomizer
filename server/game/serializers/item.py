from rest_framework import serializers

from game.models import Item

class ItemSerializer(serializers.ModelSerializer):
    type = serializers.StringRelatedField()
    rarities = serializers.StringRelatedField(many=True)
    class Meta:
        model = Item
        fields = [
            "id",
            "name",
            "type",
            "rarities",
            "base_charges",
            "overlay",
        ]
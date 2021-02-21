from rest_framework import serializers

from game.models import Item

class ItemSerializer(serializers.ModelSerializer):
    rarity = serializers.StringRelatedField()
    class Meta:
        model = Item
        fields = "__all__"
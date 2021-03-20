from rest_framework import serializers

from game.models import Item

class ItemSerializer(serializers.ModelSerializer):
    rarities  = serializers.StringRelatedField(many=True)
    class Meta:
        model = Item
        fields = "__all__"
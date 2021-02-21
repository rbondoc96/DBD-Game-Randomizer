from rest_framework import serializers

from game.models import Event 

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
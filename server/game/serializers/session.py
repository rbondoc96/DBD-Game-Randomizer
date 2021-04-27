from rest_framework import serializers

from game.models import Session
from game.serializers import PlayerSerializer, RealmSerializer

class SessionSerializer(serializers.ModelSerializer):
    host = PlayerSerializer()
    players = PlayerSerializer(many=True)
    realm = RealmSerializer()
    obsession = PlayerSerializer()
    
    class Meta:
        model = Session
        fields = "__all__"

class SessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = "__all__"
from asgiref.sync import async_to_sync

from django.dispatch import receiver
from django.db.models.signals import m2m_changed

from channels.layers import get_channel_layer

from game.models import Session
from game.serializers import SessionSerializer

@receiver(m2m_changed, sender=Session.players.through)
def session_players_changed(sender, instance, *args, **kwargs):
    if kwargs["action"] == "pre_add":
        print(f"Added into: {instance}")
        
        players = instance.players.all()
        if len(players) == 0:
            print("no players. adding 1st")
        elif len(players) < 5:
            print("not capacity")
        elif len(players) >= 5:
            print("Room is at capacity")

    if kwargs["action"] == "post_remove":
        players = instance.players.all()

        if len(players) == 0:
            print("no players left. removing")
            
            try:
                instance.delete()
            except:
                print("Delete failed")

    channel_layer = get_channel_layer()
    session_id = instance.session_id
    group_name = f"session-{session_id}"

    serializer = SessionSerializer(instance)

    event = {
        "type": "session_data",
        "session": serializer.data,
    }

    async_to_sync(channel_layer.group_send)(
        group_name,
        event
    )
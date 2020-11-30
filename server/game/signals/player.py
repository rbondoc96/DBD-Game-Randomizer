from asgiref.sync import async_to_sync

from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed

from channels.layers import get_channel_layer

from game.models import Player
from game.serializers import SessionSerializer

# When a Player updates, send send updated data to session group

@receiver(m2m_changed, sender=Player.perks.through)
def player_updated_perks(sender, instance, *args, **kwargs):
    if kwargs["action"] == "post_add":
        if instance.sessions.count() > 0:
            session = instance.sessions.all()[0]
            group_name = f"session-{session.session_id}"

            channel_layer = get_channel_layer()
            serializer = SessionSerializer(session)

            event = {
                "type": "session_data",
                "session": serializer.data,
            }

            async_to_sync(channel_layer.group_send)(
                group_name,
                event
            )

@receiver(post_save, sender=Player)
def player_updated(sender, instance, *args, **kwargs):
    print(instance)
    print(instance.sessions.count())
    if instance.sessions.count() > 0:
        session = instance.sessions.all()[0]
        group_name = f"session-{session.session_id}"

        channel_layer = get_channel_layer()
        serializer = SessionSerializer(session)

        event = {
            "type": "session_data",
            "session": serializer.data,
        }

        async_to_sync(channel_layer.group_send)(
            group_name,
            event
        ) 
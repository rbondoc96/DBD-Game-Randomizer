from asgiref.sync import async_to_sync

from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed

from channels.layers import get_channel_layer

from game.utils.logs import Logger

from game.models import Session
from game.serializers import SessionSerializer

TAG = "SessionSignals"
logger = Logger(TAG)

@receiver(post_save, sender=Session)
def session_changed(sender, instance, *args, **kwargs):
    channel_layer = get_channel_layer()
    session_id = instance.session_id
    group_name = f"session-{session_id}"

    serializer = SessionSerializer(instance)

    event = {
        "type": "session_data",
        "session": serializer.data,
    }

    logger.debug(
        f"Session Info changed", 
        "Sending updated session."
    )    

    async_to_sync(channel_layer.group_send)(
        group_name,
        event
    )    

@receiver(m2m_changed, sender=Session.players.through)
def session_players_changed(sender, instance, *args, **kwargs):
    if kwargs["action"] == "pre_add":
        logger.debug(f"Added into session: {instance}")
        
        players = instance.players.all()
        if len(players) == 0:
            logger.debug("no players. adding 1st")
        elif len(players) < 5:
            logger.debug("not capacity")
        elif len(players) >= 5:
            logger.debug("Room is at capacity")

    if kwargs["action"] == "post_remove":
        logger.debug("Player removed from session")
        players = instance.players.all()
        
        # Host left the session
        if instance.host not in players and len(players) > 0:
            instance.host = players[0]
            instance.save()

        elif len(players) <= 0:
            logger.debug("No players left. Deleting session")

            try:
                instance.delete()
            except:
                logger.error("Delete Session failed")
            return

    decide_obsession(instance)

    channel_layer = get_channel_layer()
    session_id = instance.session_id
    group_name = f"session-{session_id}"

    serializer = SessionSerializer(instance)

    event = {
        "type": "session_data",
        "session": serializer.data,
    }

    logger.debug(
        f"# of session players changed", 
        "Sending updated session."
    )    

    async_to_sync(channel_layer.group_send)(
        group_name,
        event
    )

def decide_obsession(session):
    logger.debug("Deciding Obsession")
    players = session.players.all()

    player_lucks = [{
        "player": p,
        "luck": 0
    } for p in players]

    for pl in player_lucks:
        player = pl["player"]
        perks = player.perks.all()

        for perk in perks:
            name = str(perk.name).lower()

            if name in [
                "blood pact",
                "for the people",
            ]:
                pl["luck"] -= 1

            elif name in [
                "decisive strike",
                "mettle of man",
                "object of obsession",
                "sole survivor"
            ]:
                pl["luck"] += 1
          

    # Find dict with the largest luck
    max_val = 0
    max_idx = 0
    for idx in range(0, len(player_lucks)):
        pl = player_lucks[idx]
        max_idx = idx if pl["luck"] > max_val else max_idx        
        max_val = pl["luck"] if pl["luck"] > max_val else max_val
    

    # There is an obsession to be found
    if max_val != 0:
        max_pl = player_lucks.pop(max_idx)

        if len(player_lucks) > 0:
            new_max = 0
            for pl in player_lucks:
                new_max = pl["luck"] if pl["luck"] > new_max else new_max

            obsession = None if new_max == max_val else max_pl["player"]

        else:
            obsession = max_pl["player"]

    else:
        obsession = None

    session.obsession = obsession

    logger.debug("Obsession", obsession)

    return session    
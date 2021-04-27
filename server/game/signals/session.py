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
        print(f"Added into session: {instance}")
        
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
            logger.debug("no players left. removing")
            
            try:
                instance.delete()
                return
            except:
                logger.error("Delete failed")
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
    players_luck = [0 for p in players]

    player_lucks = [{
        "player": p,
        "luck": 0
    } for p in players]

    for pl in player_lucks:
        player = pl["player"]
        perks = player.perks.all()

        for perk in perks:
            logger.debug(pl["player"], pl["luck"])
            
            if perk.name == "Blood Pact":
                pl["luck"] -= 1
            elif perk.name == "Decisive Strike":
                pl["luck"] += 1
            elif perk.name == "For the People":
                pl["luck"] -= 1
            elif perk.name == "Mettle of Man":
                pl["luck"] += 1
            elif perk.name == "Object of Obsession":
                pl["luck"] += 1
            elif perk.name == "Sole Survivor":
                pl["luck"] += 1

            logger.debug(pl["player"], pl["luck"])                

    # Find dict with the largest luck
    max_val = 0
    max_idx = 0
    for idx in range(0, len(player_lucks)):
        pl = player_lucks[idx]
        max_idx = idx if pl["luck"] > max_val else max_idx        
        max_val = pl["luck"] if pl["luck"] > max_val else max_val
    
    logger.debug("Val", max_val, "Idx", max_idx)

    # There is an obsession to be found
    if max_val != 0:
        logger.debug(player_lucks)
        max_pl = player_lucks.pop(max_idx)
        logger.debug("PL", pl)

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
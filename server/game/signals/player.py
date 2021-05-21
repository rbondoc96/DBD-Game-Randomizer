from asgiref.sync import async_to_sync

from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed

from channels.layers import get_channel_layer

from game.utils.logs import Logger

from game.models import Player, Realm, Offering
from game.serializers import SessionSerializer

TAG = "PlayerSignals"
logger = Logger(TAG)

# When a Player updates, send send updated data to session group

@receiver(m2m_changed, sender=Player.perks.through)
def player_updated_perks(sender, instance, *args, **kwargs):

    if kwargs["action"] == "post_add":
        if instance.sessions.count() > 0:
            session = instance.sessions.all()[0]

            # logger.debug(
            #     f"Perks for {instance} changed", 
            #     "Sending updated session."
            # )

            # send_updated_session(session)              

@receiver(post_save, sender=Player)
def player_updated(sender, instance, *args, **kwargs):

    logger.debug(instance)
    logger.debug(instance.sessions.count())

    if instance.sessions.count() > 0:
        session = instance.sessions.all()[0]

        logger.debug(
            f"Instance {instance} updated", 
            "Sending updated session."
        )  

        decide_obsession(session)
        decide_realm(session)
        send_updated_session(session)   

def decide_realm(session):
    logger.debug("Deciding Realm")
    players = session.players.all()
    offerings = [p.offering for p in players]
    realms = []
    sacrificial_ward_exists = False

    for offering in offerings:
        if offering is None:
            continue

        realm = None        

        if offering.name == "MacMillan's Phalanx Bone":
            realm = Realm.objects.get(name="The Macmillan Estate")
        elif offering.name == "Azarov's Key":
            realm = Realm.objects.get(name="Autohaven Wreckers")
        elif offering.name == "Heart Locket":
            realm = Realm.objects.get(name="Coldwind Farm")
        elif offering.name == "Charred Wedding Photograph":
            realm = Realm.objects.get(name="Crotus Prenn Asylum")
        elif offering.name == "Strode Realty Key":
            realm = Realm.objects.get(name="Haddonfield")
        elif offering.name == "Shattered Glasses":
            realm = Realm.objects.get(name="Léry's Memorial Institute")
        elif offering.name == "Grandma's Cookbook":
            realm = Realm.objects.get(name="Backwater Swamp")
        elif offering.name == "The Last Mask":
            realm = Realm.objects.get(name="Red Forest")
        elif offering.name == "The Pied Piper":
            realm = Realm.objects.get(name="Springwood")
        elif offering.name == "Jigsaw Piece":
            realm = Realm.objects.get(name="Gideon Meat Plant")
        elif offering.name == "Yamaoka Family Crest":
            realm = Realm.objects.get(name="Yamaoka Estate")
        elif offering.name == "Damaged Photo":
            realm = Realm.objects.get(name="Ormond")
        elif offering.name == "Hawkins National Laboratory ID":
            realm = Realm.objects.get(name="Hawkins National Laboratory")
        elif offering.name == "Dusty Noose":
            realm = Realm.objects.get(name="Grave of Glenvale")
        elif offering.name == "Mary's Letter":
            realm = Realm.objects.get(name="Silent Hill")
        elif offering.name == "Sacrificial Ward":
            sacrificial_ward_exists = True
        
        if realm is not None:
            realms.append(realm)

    if sacrificial_ward_exists:
        if len(realms) == 4:
            if realms[0] == realms[1] and realms[1] == realms[2] and \
                realms[2] == realms[3]:
                sacrificial_ward_exists = False

    # if sacrificial_ward_exists is still True, then Realm is unknown
    if sacrificial_ward_exists:
        session.realm = None

    else:
        uniques = set(realms)
        
        if len(uniques) == 1:
            session.realm = realms[0]
        else:
            # Realm is unknown
            session.realm = None

    return session
        

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

    # Find dict with the largest luck
    max_val = 0
    max_idx = 0
    for idx in range(0, len(player_lucks)):
        pl = player_lucks[idx]
        max_idx = idx if pl["luck"] > max_val else max_idx        
        max_val = pl["luck"] if pl["luck"] > max_val else max_val

    # There is an obsession to be found
    obsession = None
    if max_val != 0:
        max_pl = player_lucks.pop(max_idx)

        if len(player_lucks) > 0:
            new_max = 0
            for pl in player_lucks:
                new_max = pl["luck"] if pl["luck"] > new_max else new_max

            obsession = None if new_max == max_val else max_pl["player"]

        else:
            obsession = max_pl["player"]

    session.obsession = obsession
    return session


def send_updated_session(session):
    channel_layer = get_channel_layer()

    serializer = SessionSerializer(session)
    group_name = f"session-{session.session_id}"

    event = {
        "type": "session_data",
        "session": serializer.data,
    }

    async_to_sync(channel_layer.group_send)(
        group_name,
        event
    )     
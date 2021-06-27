from random import sample, randint, choice as random_choice

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from game.utils.error import ErrorResponse, ErrorTypes
from game.utils.logs import Logger
from game.models import(
    Session,
    Player,
    Character,
    Offering,
    Perk,
    Item, Power,
    ItemAddOn, PowerAddOn,
)
from game.serializers import(
    SessionSerializer,
    SessionCreateSerializer,
    PlayerSerializer,
    PlayerCreateSerializer,
    PerkSerializer,
)

from game.utils import get_random_index
from game.utils.player import PlayerUtils
from game.utils.session import SessionUtils

TAG = "SessionAPI"
logger = Logger(TAG)

def randomize_player(instance, role, no_licensed_chars=False):
    # Auto Survivor assignment may avoid issue with 2+ Killers in a session
    if(role is None):
        role = "Survivor"

    role__proper = role.title()
    
    instance.role = role__proper

    # Get random Character based off role and restrictions
    characters = Character.objects.filter(type=role__proper)
    if no_licensed_chars:
        characters = characters.exclude(is_licensed=True)
    
    character = random_choice(characters)
    instance.character = character

    # Get random Player offering
    offering = None
    if randint(0,3):
        if role.lower() == "survivor":
            offerings = Offering.objects.exclude(type="Killer")
        else:
            offerings = Offering.objects.exclude(type="Survivor")

        offering = random_choice(offerings)
        instance.offering = offering

    
    # Get random Player resource (Item or Power)
    # Must reset Player resource from previous randomization
    instance.item = None;
    instance.power = None;
    if role.lower() == "survivor":
        items = Item.objects.all()
        item = random_choice(items)
        instance.item = item
    else:
        instance.power = instance.character.power

    # Get random add-ons
    # Must reset resource addons
    instance.item_addons.clear()
    instance.power_addons.clear()
    if instance.item is not None:
        addon_set = ItemAddOn.objects.filter(
            type=instance.item.type
        )

        for _ in range(0, 2):    
            if len(addon_set) > 0:
                addon = random_choice(addon_set)
                instance.item_addons.add(addon)
            else:
                addon = None

            print("Addon:", addon)

    else:
        addon_set = PowerAddOn.objects.filter(
            power=instance.power
        )
        
        for _ in range(0, 2):
            if len(addon_set) == 1:
                addon = addon_set[0]
                instance.power_addons.add(addon)
            else:
                addon = None

            print("Addon", addon)        


    perk_set = Perk.objects.filter(type=role__proper)
    instance.perks.clear()
    
    while instance.perks.count() < 4:
        perk = random_choice(perk_set)

        if (perk in instance.perks.all()) and \
            (perk_set.count() > 4):
            while perk in instance.perks.all():
                perk = random_choice(perk_set)
                    
        instance.perks.add(perk)
        
    instance.save()
    return instance

def generate_player(role="survivor", no_licensed_chars=False):
    role__proper = role.title()
    player = {
        "role": role__proper,
    }

    if no_licensed_chars:
        characters = Character.objects.filter(
            type=role__proper,
        ).exclude(is_licensed=True)
    else:
        characters = Character.objects.filter(type=role__proper)
    
    character = characters[get_random_index(characters)]
    player["character"] = character

    offering = None
    if randint(0,3):
        offerings = Offering.objects.all()
        offering = offerings[get_random_index(offerings)]
        player["offering"] = offering
    
    item = None
    power = None
    if role == "survivor":
        items = Item.objects.all()
        item = items[get_random_index(items)]
        player["item"] = item

    elif role == "killer":
        power = Power.objects.all()[0]
        player["power"] = power

    PLAYER = Player.objects.create(
        **player
    )

    perk_set = Perk.objects.filter(type=role__proper)
    for _ in range(0, 4):
        PLAYER.perks.add(
            perk_set[get_random_index(perk_set)]
        )
    PLAYER.save()
    return PLAYER

def generate_session(mode, host, num_players=1):
    data = {
        "mode": mode.title(),
        "host": host,
    }
    
    session = Session.objects.create(
        **data,
    )
    session.players.add(host)
    session.save()

    return session

def reverse_player_role(player):

    reverse_role = "survivor" if player.role.lower() == "killer" else "killer"

    # Temporary instance
    new_player = generate_player(role=reverse_role)
    new_data = PlayerCreateSerializer(new_player).data

    # Don't need these fields when updating an existing field
    del new_data["id"]
    del new_data["player_id"]
    new_player.delete()
    
    serializer = PlayerCreateSerializer(
        player, 
        data=new_data,     
        partial=True,
    )

    if serializer.is_valid():
        print("Successfully changed role")
        return serializer.save()
    else:
        print("Role change unsuccessful")    
        return player





class SessionAPI(APIView):

    def create_session(self, player):
        pass       


    def get(self, request, *args, **kwargs):
        params = request.query_params
        action = params.get("action")

        if action is None:
            return Response({
                "error": "Please specify an action",
            }, status=status.HTTP_400_BAD_REQUEST)

        player = PlayerUtils.get_client_player(request)

        session = None
        if action.lower() == "join":
            sid = params.get("sessionId")

            if sid is None:
                err = ErrorResponse(
                    ErrorTypes.NoSessionIdGiven.code,
                    "Please provide a session ID."
                )
                return Response(
                    err.message(), 
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                session = SessionUtils.join_session(sid, player)
            
            except ErrorTypes.UnsupportedSessionMode as e_mode:
                err = ErrorResponse(
                    e_mode.code,
                    "Critical Error! Session is assigned an unsupported mode."
                )
                return Response(
                    err.message(), 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            except ErrorTypes.SessionIsFull as e_full:
                err = ErrorResponse(
                    e_full.code,
                    f"Session {sid} is full"
                )
                return Response(
                    err.message(), 
                    status=status.HTTP_400_BAD_REQUEST
                )

            if session is None:
                err = ErrorResponse(
                    ErrorTypes.NoSessionWithMatchingId.code,
                    "There are no sessions with that session ID"
                )
                return Response(
                    err.message(), 
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response({
                "session": SessionSerializer(session).data,
            }, status=status.HTTP_202_ACCEPTED)                            


        elif action.lower() == "create":
            mode = params.get("mode")

            if mode is None:
                return Response({
                    "message": "Session mode must be specified"
                }, status=status.HTTP_400_BAD_REQUEST)    
            
            mode = str(mode).title()
                
            try:
                session = SessionUtils.create_session(mode, player)

            except ErrorTypes.UnsupportedSessionMode as e_mode:
                err = ErrorResponse(
                    e_mode.code,
                    "Session mode is not supported."
                )
                return Response(
                    err.message(), 
                    status=status.HTTP_400_BAD_REQUEST
                )

            if session is None:
                err = ErrorResponse(
                    ErrorTypes.UnableToCreateSession.code,
                    "Critical Error! Server could not create a new session."
                )
                return Response(
                    err.message(),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            return Response({
                "session": SessionSerializer(session).data,
            }, status=status.HTTP_201_CREATED)

 
        elif action.lower() == "changehost":
            new_host_id = params.get("newHostId")
            session_id = params.get("sessionId")

            if new_host_id is None:
                err = ErrorResponse(
                    ErrorTypes.NoHostIdGiven.code,
                    "New Player host ID was not provided."
                )
                return Response(
                    err.message(),
                    status=status.HTTP_400_BAD_REQUEST
                )

            if session_id is None:
                err = ErrorResponse(
                    ErrorTypes.NoSessionIdGiven.code,
                    "Session ID was not provided."
                )
                return Response(
                    err.message(),
                    status=status.HTTP_400_BAD_REQUEST
                )                
            
            try:
                SessionUtils.switch_host(session_id, new_host_id)

            except ErrorTypes.NoSessionWithMatchingId as e_session:
                err = ErrorResponse(
                    ErrorTypes.NoSessionWithMatchingId.code,
                    f"Session with ID {session_id} could not be found."
                )
                return Response(
                    err.message(),
                    status=status.HTTP_400_BAD_REQUEST
                ) 

            except ErrorTypes.NoPlayerWithMatchingId as e_player:
                err = ErrorResponse(
                    ErrorTypes.NoPlayerWithMatchingId.code,
                    f"Player with ID {new_host_id} could not be found."
                )
                return Response(
                    err.message(),
                    status=status.HTTP_400_BAD_REQUEST
                ) 

            return Response({
                "message": "Session host changed"
            }, status=status.HTTP_200_OK)            


        else:
            return Response({
                "error": f"Action <<{action}>> not supported"
            }, status=status.HTTP_400_BAD_REQUEST)
    

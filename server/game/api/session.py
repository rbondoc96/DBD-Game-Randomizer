from random import sample, randint, choice as random_choice

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

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
    def get(self, request, *args, **kwargs):

        params = request.query_params
        action = params.get("action")

        if action is not None:
            player = request.session.get("player")              

            if action.lower() == "join":
                session_id = params.get("sessionId")

                if session_id is not None:
                    session = None
                    try:
                        session_id__proper = str(session_id).upper()
                        session = Session.objects.get(
                            session_id=session_id__proper
                        )
                        logger.debug("Existing session acquired.")

                    except Session.DoesNotExist:
                        return Response({
                            "error": \
                            "There are no sessions with that session ID."
                            }, status=status.HTTP_400_BAD_REQUEST)

                    if session.mode.lower() == "survivor":
                        if player is not None:
                            player_id = player.get("player_id")

                            try:
                                player = Player.objects.get(player_id=player_id)
                                logger.debug("Acquired existing player")

                                if player.role is None:
                                    player = randomize_player(
                                        player,
                                        role="survivor"
                                    )

                                elif player.role.lower() == "killer":
                                    player = reverse_player_role(
                                        player,
                                        no_licensed_chars,
                                    )
                            
                            except Player.DoesNotExist:
                                player = generate_player(
                                    role="survivor",
                                    no_licensed_chars=no_licensed_chars,
                                )
                                request.session["playerId"] = player.player_id
                        else:
                            logger.debug("Generating new player")
                            player = generate_player(
                                role="survivor",
                            )
                            request.session["playerId"] = player.player_id

                        if player in session.players.all():
                            pass
                        else:
                            if session.players.count() >= 4:
                                return Response({
                                    "error": "Session room is already full",
                                }, status=status.HTTP_226_IM_USED)

                            else:
                                logger.debug(f"Adding player to session {session.session_id}")
                                session.players.add(player)
                                session.save()

                    return Response({
                        "session": SessionSerializer(session).data,
                    }, status=status.HTTP_202_ACCEPTED)                            

            elif action.lower() == "create":
                mode = params.get("mode")

                if mode is None:
                    return Response({
                        "message": "Session mode must be specified"
                    }, status=status.HTTP_400_BAD_REQUEST)    
                
                mode = str(mode).lower()
                    
                if mode == "survivor":
                    if player is not None:
                        session = None

                        try:
                            # Get actual Player model instance from 
                            # request["session"]["player"]
                            player_id = player.get("player_id")
                            player = Player.objects.get(player_id=player_id)
                            logger.debug("Found existing player")

                        except Player.DoesNotExist:
                            logger.warn("Player did not exist. Creating a new one")
                            player = generate_player(role="survivor")    
                            request.session["player"] = PlayerSerializer(
                                player
                            ).data

                        # If player doesn't have any Player data
                        if player.role is None:
                            player = randomize_player(player, role="survivor")

                        # Convert player to survivor 
                        elif player.role.lower() == "killer":
                            player = reverse_player_role(player)

                        try:
                            # Check for & grab existing session, if it exists
                            session = Session.objects.get(host=player)
                            serializer = SessionSerializer(session)
                            return Response({
                                "session": serializer.data
                            }, status=status.HTTP_200_OK)

                        except Session.DoesNotExist:
                            logger.warn(f"Player {player.player_id} not hosting any sessions. Creating one.")

                            session = generate_session(
                                mode="survivor",
                                host=player,
                            )

                        return Response({
                            "session": SessionSerializer(session).data,
                        }, status=status.HTTP_201_CREATED)

                elif mode == "custom":
                    if player is not None:
                        session = None

                        try:
                            # Get actual Player model instance
                            player_id = player.get("player_id")
                            player = Player.objects.get(player_id=player_id)

                        except Player.DoesNotExist:
                            print("Player did not exist. Creating a new one")
                            player = generate_player(role="killer")    
                            request.session["player"] = PlayerSerializer(
                                player
                            ).data

                        try:
                            # Check for & grab existing session, if it exists
                            session = Session.objects.get(host=player)
                            serializer = SessionSerializer(session)
                            
                            return Response({
                                "session": serializer.data
                            }, status=status.HTTP_200_OK)

                        except Session.DoesNotExist:
                            print(f"Player {player.player_id} not hosting any sessions. Creating one.")

                            # Convert player to killer, the host must be the killer
                            if player.role.lower() == "survivor":
                                player = reverse_player_role(player)

                            session = generate_session(
                                mode="custom",
                                host=player,
                            )

                            print("Session", session)

                        return Response({
                            "session": SessionSerializer(session).data,
                        }, status=status.HTTP_201_CREATED) 


                    return Response({
                        "session": SessionSerializer(session).data,
                        "playerId": request.session["playerId"]
                    }, status=status.HTTP_201_CREATED)     

                else:
                    return Response({
                        "error": "Session mode not supported"
                    }, status=status.HTTP_400_BAD_REQUEST)               

            else:
                return Response({
                    "error": f"Action <<{action}>> not supported"
                }, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response({
                "error": "Please specify an action",
            }, status=status.HTTP_400_BAD_REQUEST)

        num_players = params.get("numPlayers")
        no_licensed_chars = bool(params.get("nonLicensedOnly"))

        player = None
        player_id = request.session.get("playerId")

        print("Id", player_id)

        return Response({
            "message": action
        }, status=status.HTTP_200_OK)

        if num_players <= 0 or num_players > 5:
            return Response({
                "error": "Number of Players must be between 1 and 5."
            }, status=status.HTTP_400_BAD_REQUEST)

        if session_id is not None:
            try:
                if session.mode.lower() == "survivor":
                    if player_id is not None:
                        try:
                            player = Player.objects.get(player_id=player_id)
                            print("Acquired existing player")

                            if player.role.lower() == "killer":
                                player = reverse_player_role(
                                    player,
                                    no_licensed_chars,
                                )
                        
                        except Player.DoesNotExist:
                            player = generate_player(
                                role="survivor",
                                no_licensed_chars=no_licensed_chars,
                            )
                            request.session["playerId"] = player.player_id
                    else:
                        print("Generating new player")
                        player = generate_player(
                            role="survivor",
                            no_licensed_chars=no_licensed_chars,
                        )
                        request.session["playerId"] = player.player_id

                    if player in session.players.all():
                        pass
                    else:
                        if session.players.count() >= 4:
                            return Response({
                                "error": "Session room is already full",
                            }, status=status.HTTP_226_IM_USED)

                        else:
                            print(f"Adding player to session {session.session_id}")
                            session.players.add(player)
                            session.save()

                return Response({
                    "session": SessionSerializer(session).data,
                }, status=status.HTTP_202_ACCEPTED)
            except Session.DoesNotExist:
                return Response({
                    "error": "There are no sessions with that session ID."
                }, status=status.HTTP_400_BAD_REQUEST)

        else:
            if mode == "killer":
                if num_players > 1:
                    return Response({
                        "error": "Killer sessions may only have up to 1 player"
                    })

                if player_id is not None:
                    try:
                        player = Player.objects.get(player_id=player_id)
                        
                        # Convert player to a survivor before moving forward
                        if player.role.lower() == "survivor":
                            player = reverse_player_role(
                                player, 
                                no_licensed_chars
                            )
                    
                        print("Acquired existing player. Checking for an existing session.")

                        session = Session.objects.get(host=player)
                        serializer = SessionSerializer(session)

                        return Response({
                            "session": serializer.data
                        }, status=status.HTTP_200_OK)

                    except Player.DoesNotExist:
                        print("Player did not exist. Creating a new one")
                        player = generate_player(
                            role="killer",
                            no_licensed_chars=no_licensed_chars,
                        )    
                        request.session["playerId"] = player.player_id  

                    except Session.DoesNotExist:
                        print(f"Player {player.player_id} not hosting any sessions. Creating one.")
                        session = generate_session(
                            mode="killer",
                            host=player,
                        )
                        return Response({
                            "session": SessionSerializer(session).data,
                        }, status=status.HTTP_201_CREATED)

                else:
                    player = generate_player(
                        role="killer",
                        no_licensed_chars=no_licensed_chars,
                    )    
                    request.session["playerId"] = player.player_id  

                    session = generate_session(
                        mode="killer",
                        host=player,
                    )

                    return Response({
                        "session": SessionSerializer(session).data,
                        "playerId": request.session["playerId"]
                    }, status=status.HTTP_201_CREATED)
                
            elif mode == "survivor":
                if num_players > 4:
                    return Response({
                        "error": "Survivor sessions may only have up to 4 players"
                    })

                if player_id is not None:
                    try:
                        player = Player.objects.get(player_id=player_id)
                        
                        # Convert player to a survivor before moving forward
                        if player.role.lower() == "killer":
                            player = reverse_player_role(
                                player, 
                                no_licensed_chars
                            )
                    
                        print("Acquired existing player. Checking for an existing session.")

                        session = Session.objects.get(host=player)
                        serializer = SessionSerializer(session)

                        return Response({
                            "session": serializer.data
                        }, status=status.HTTP_200_OK)

                    except Player.DoesNotExist:
                        print("Player did not exist. Creating a new one")
                        player = generate_player(
                            role="survivor",
                            no_licensed_chars=no_licensed_chars,
                        )    
                        request.session["playerId"] = player.player_id  

                    except Session.DoesNotExist:
                        print(f"Player {player.player_id} not hosting any sessions. Creating one.")
                        session = generate_session(
                            mode="survivor",
                            host=player,
                        )
                        return Response({
                            "session": SessionSerializer(session).data,
                        }, status=status.HTTP_201_CREATED)

                else:
                    player = generate_player(
                            role="survivor",
                            no_licensed_chars=no_licensed_chars,
                        )    
                    request.session["playerId"] = player.player_id  

                    session = generate_session(
                        mode="killer",
                        host=player,
                    )

                    return Response({
                        "session": SessionSerializer(session).data,
                        "playerId": request.session["playerId"]
                    }, status=status.HTTP_201_CREATED)
                   
            else:
                if num_players < 2:
                    return Response({
                        "error": "Custom sessions must have at least 2 players"
                    })
                if num_players > 5:
                    return Response({
                        "error": "Custom sessions may only have up to 5 players"
                    })

                if player_id is not None:
                    pass
                else:
                    pass
            # Current player role will stay
            # Other player roles will generate based on Host                 

    def post(self, request, *args, **kwargs):
        data = request.data
        print(data)

        # session = generate_session()

        return Response({**data}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        pass
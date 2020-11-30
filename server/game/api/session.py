from random import sample, randint

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

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

def get_rand_index(iterable):
    return sample(range(0, len(iterable)), 1)[0]

def get_addons(model):
    pass

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
    
    character = characters[get_rand_index(characters)]
    player["character"] = character

    offering = None
    if randint(0,3):
        offerings = Offering.objects.all()
        offering = offerings[get_rand_index(offerings)]
        player["offering"] = offering
    
    item = None
    power = None
    if role == "survivor":
        items = Item.objects.all()
        item = items[get_rand_index(items)]
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
            perk_set[get_rand_index(perk_set)]
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

    # if num_players > 2 and (mode == "survivor" or mode == "custom"):
    #     if host.role() == "killer":
    #         # Generate survivors
    #         pass
    #     else: 
    #         # Generate 1 killer and see if extra survivors are needed
    #         pass

    return session

def reverse_player_role(player, no_licensed_chars=False):
    print("Changing roles")

    reverse_role = "survivor" if player.role.lower() == "killer" else "killer"

    # Temporary instance
    new_player = generate_player(
        role=reverse_role,
        no_licensed_chars=no_licensed_chars,
    )
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
        session_id = params.get("sessionId")
        mode = str(params.get("mode")).lower()
        num_players = int(params.get("numPlayers"))
        no_licensed_chars = bool(params.get("nonLicensedOnly"))
        
        player = None
        player_id = request.session.get("playerId")

        if num_players <= 0 or num_players > 5:
            return Response({
                "error": "Number of Players must be between 1 and 5."
            }, status=status.HTTP_400_BAD_REQUEST)

        if session_id is not None:
            try:
                session_id__proper = str(session_id).upper()
                session = Session.objects.get(session_id=session_id__proper)

                print("Existing session acquired.")

                if session.mode.lower() == "killer":
                    return Response({
                        "error": "Killer sessions are single player only."
                    }, status=status.HTTP_400_BAD_REQUEST)

                elif session.mode.lower() == "survivor":
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

    def delete(self, request, *args, **kwargs):
        pass
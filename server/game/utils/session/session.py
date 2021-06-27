from rest_framework import status
from rest_framework.response import Response

from game.models import Session, Player
from game.utils.error import ErrorTypes
from game.utils.player import PlayerUtils

class SessionUtils:
    
    @staticmethod
    def find_session(sid):
        session = None
        try:
            session_id = str(sid).upper()
            session = Session.objects.get(
                session_id=session_id
            )

        except Session.DoesNotExist:
            return None
        
        return session


    @staticmethod
    def switch_host(sid, hid):
        
        session = None
        host = None
        try:
            session = Session.objects.get(
                session_id=sid
            )      
            host = Player.objects.get(
                player_id=hid
            )       

        except Session.DoesNotExist:
            raise ErrorTypes.NoSessionWithMatchingId

        except Player.DoesNotExist:
            raise ErrorTypes.NoPlayerWithMatchingId      

        if host.role.lower() != "killer":
            host = PlayerUtils.reverse_role(host)

        session.host = host
        session.save()
        return session


    @staticmethod
    def create_session(mode, player):
        session = None

        if mode != "survivor" and mode != "custom":
            raise ErrorTypes.UnsupportedSessionMode

        if player is None:
            player = PlayerUtils.generate("Survivor")

        try:
            session = Session.objects.get(host=player)

        except Session.DoesNotExist:
            pass

        if session is None:

            if (mode == "survivor" and player.role.lower() != "survivor") or \
                (mode == "custom" and player.role.lower() != "killer"):
                player = PlayerUtils.reverse_role(player)
            
            session = Session.objects.create(
                mode=mode,
                host=player
            )
            session.players.add(player)
            session.save()

        return session
    

    @staticmethod
    def join_session(sid, player):
        session = SessionUtils.find_session(sid)
        
        if session is None:
            return None

        max_players = 4
        mode = session.mode.lower()
        if mode == "survivor" and player.role.lower() == "killer":
            
            player = PlayerUtils.reverse_role(player)

        elif mode == "custom":
            max_players = 5
            if session.host is None and player.role.lower() == "survivor":
                player = PlayerUtils.reverse_role(player)
                session.host = player
                session.save()

        elif mode != "custom" and mode != "survivor":
            raise ErrorTypes.UnsupportedSessionMode

        if player not in session.players.all():
            if session.players.count() >= max_players:
                raise ErrorTypes.SessionIsFull

            else:
                session.players.add(player)
                session.save()    

        return session         
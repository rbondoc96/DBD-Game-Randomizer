import re
import json
import asyncio
from random import randint, sample
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from game.utils.logs import Logger
from game.models import (
    Session, 
    Player, 
    Perk, 
    Item, Power, 
    Character,
    Offering,
)
from game.serializers import SessionSerializer, PlayerCreateSerializer
from game.utils import get_random_index, generate_random_player

TAG = "SessionConsumer"
logger = Logger(TAG)

def get_rand_index(iterable):
    return sample(range(0, len(iterable)), 1)[0]



class SessionConsumer(AsyncWebsocketConsumer):
    
    # User connects to Consumer through "ws://" URL
    async def connect(self):
        print("connecting to ws client")

        # <<self.scope>> is similar to <<request>> in Django views
        # <<self.scope["url_route"]>> - A dict with 2 keys: "kwargs" and "args"
        # "kwargs" is a dict of named regex groups

        # Grabs the <<session_id>> from the Websocket's URL
        self.session_id = self.scope["url_route"]["kwargs"]["session_id"]
        self.session_group_name = f"session-{self.session_id}"

        # Grab the Player stored in the session, if it exists
        self.player = await database_sync_to_async(
            self.scope["session"].get)("player")

        self.player_id = await database_sync_to_async(
            self.player.get)("player_id")

        # A session is a 6 character alphanumeric string
        session_regex = re.compile(r"^([a-zA-Z0-9]{6})$")
        
        if session_regex.match(self.session_id) is not None:
            
            if self.player_id is not None:
                print("Looking for existing player with ID#", self.player_id)
                try:
                    self.player = await database_sync_to_async(
                        Player.objects.get)(player_id=self.player_id)

                    print("Acquired existing player:", self.player)
                    
                except Player.DoesNotExist:
                    print("Player did not exist. Creating a new one")

                    self.player = await self.generate_player("survivor")
                    self.scope["session"]["player"] = self.player
                    await database_sync_to_async(self.scope["session"].save)()

                    self.player_id = await database_sync_to_async(
                        self.player.get)("player_id")
            
            else:
                print("Creating a new player")
                
                self.player = await self.generate_player("survivor")
                self.scope["session"]["player"] = self.player
                await database_sync_to_async(self.scope["session"].save)()
                
                self.player_id = await database_sync_to_async(
                    self.player.get)("player_id")

            # Look for existing session first before making a new one
            try:
                self.session = await database_sync_to_async(
                    Session.objects.get)(session_id=self.session_id)

            except Session.DoesNotExist:
                print("This session does not exist.")
                return

            print("Acquired existing session", self.session)
            session_players = await self.get_session_players()

            if not self.player in session_players:
                print("Player not in session")
                if len(session_players) < 4 and \
                    self.session.mode.lower() == "survivor":
                    
                    await database_sync_to_async(
                        self.session.players.add)(self.player)
                    
                    await database_sync_to_async(
                        self.session.save)()

                    print(f"{self.player} added to survivor game")

                elif len(session_players) < 5  and \
                    self.session.mode.lower() == "custom":

                    await database_sync_to_async(
                        self.session.players.add)(self.player)
                    
                    await database_sync_to_async(
                        self.session.save)()
                    print(f"{self.player} added to custom game")

                else:
                    print("Max number of players exceeded")
            
            await self.channel_layer.group_add(
                self.session_group_name,
                self.channel_name,
            )
            await self.accept()
            await database_sync_to_async(
                self.scope["session"].save)()            
            print(f"Connected to session {self.session_id}")            
            print("Sending data...")

            serializer = await database_sync_to_async(
            SessionSerializer)(self.session)

            data = await database_sync_to_async(
                getattr)(serializer, "data")

            payload = {
                "session": data,
            }         
            await self.send(text_data=json.dumps(payload))
            print("Session data sent to", self.player_id)

        else:
            print(self.session_id)
            print("invalid session Id given")

    async def receive(self, text_data):
        # Actions
        # ["Change Player Name", "Validate Session"]
        # data = {
        #     "action": "get_random",
        #     "form": {
        #         "playerName": "",
        #         "role": "",
        #     }
        # }

        data = json.loads(text_data)

        name = data.get("playerName")
        if name is not None:
            self.player.name = name
            await database_sync_to_async(
                self.player.save)()

        print(self.player)

        # serializer = await database_sync_to_async(
        #     SessionSerializer)(self.session)

        # data = await database_sync_to_async(
        #     getattr)(serializer, "data")

        # Bug -- playerId is the previous one before socket disconnected
        # payload = {
        #     "playerId": self.player_id,
        #     "sessionId": self.session_id,
        #     "session": data,
        # }         
        
        # await self.send(text_data=json.dumps(payload))

        # print("Session data sent to", self.player_id)

    async def disconnect(self, close_code):
        if getattr(self, "session", None):
            players = await self.get_session_players()
            if self.player in players:
                await database_sync_to_async(
                    self.session.players.remove)(self.player)

            await self.channel_layer.group_discard(
                self.session_group_name,
                self.channel_name,
            )
            
            print("Socket disconnected. Player removed from session")
        

    # Handler for sending session data to all connections in the channel layer
    async def session_data(self, event):
        session = json.dumps({
            "playerId": self.player_id,
            "sessionId": self.session_id,
            "session": event.get("session"),
        })
        await self.send(text_data=session)

    @database_sync_to_async
    def get_session_players(self):
        # Must convert to a list before returning
        # Returning as a QuerySet gives Synchronous Errors
        players = list(self.session.players.all())
        return players

    @database_sync_to_async
    def generate_player(self, role, no_licensed_chars=False):
        print("Generating player...")
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

        # FIXME: Needs to return Killer's respective power
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

    @database_sync_to_async
    def generate_session(self, mode, host):
        attributes = {
            "mode": mode.title(),
            "host": host,
        }
        
        session = Session.objects.create(
            **attributes,
        )
        session.players.add(host)

        # "Custom" games require that the host is the killer
        if mode == "Custom" and host.role.lower() != "killer":

            reverse_role = "killer"

            # Temporary instance
            new_player = self.generate_player(role=reverse_role)
            new_data = PlayerCreateSerializer(new_player).data

            # Don't need these fields when updating an existing field
            del new_data["id"]
            del new_data["player_id"]
            new_player.delete()
            
            serializer = PlayerCreateSerializer(
                host, 
                data=new_data,     
                partial=True,
            )

            if serializer.is_valid():
                print("Host is now the Killer.")
                serializer.save()
            else:
                print("Role change unsuccessful")

        session.save()

        return session

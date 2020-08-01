from django.conf import settings
from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer
from .models import *
from .assets import *

game_id="randomegameid"




class LobbyConsumer(SyncConsumer):

    def websocket_connect(self, event):
        this_user_group = "denied"
        current_user = self.scope["user"]
        url_id =  self.scope["url_route"]["kwargs"]["url_id"]
        print("wuhahahhahaha" + url_id)
        #url_id = self.scope["url_id"]
        if current_user.is_authenticated:
            this_game = Game.objects.get(lobby_id=url_id)
            if is_host(current_user,this_game):
                this_user_group = "lobby-" + url_id + "-host"
                print('consumer ' + this_user_group)
            else:
                this_user_group = "lobby-" + url_id + "-queue"
            self.send({
                'type': 'websocket.accept'
            })
            # Adding the user to the appropriate group
            async_to_sync(self.channel_layer.group_add)(
                this_user_group,
                self.channel_name
            )

    def websocket_disconnect(self, event):
        this_user_group = "denied"
        current_user = self.scope["user"]
        url_id =  self.scope["url_route"]["kwargs"]["url_id"]
        if current_user.is_authenticated:
            this_game = Game.objects.get(lobby_id=url_id)
            if is_host(current_user,this_game):
                this_user_group = "lobby-" + url_id + "-host"
            else:
                this_user_group = "lobby-" + url_id + "-queue"
            self.send({
                'type': 'websocket.accept'
            })

        async_to_sync(self.channel_layer.group_discard)(
            this_user_group,
            self.channel_name
        )

    def lobby_update(self, event):
        self.send({
            'type': 'websocket.send',
            'text': str(event['content']),
        })


class GameConsumer(SyncConsumer):

    def websocket_connect(self, event):
        print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPp")
        this_user_group = "denied"
        current_user = self.scope["user"]
        url_id =  self.scope["url_route"]["kwargs"]["url_id"]
        if current_user.is_authenticated:
            this_game = Game.objects.get(game_id=url_id)
            if is_player(current_user,this_game):
                this_user_group = "game-" + url_id + "-" + str(current_user)
            self.send({
                'type': 'websocket.accept'
            })
            # Adding the user to the appropriate group
            async_to_sync(self.channel_layer.group_add)(
                this_user_group,
                self.channel_name
            )

    def websocket_disconnect(self, event):
        this_user_group = "denied"
        current_user = self.scope["user"]
        url_id =  self.scope["url_route"]["kwargs"]["url_id"]
        if current_user.is_authenticated:
            this_game = Game.objects.get(game_id=url_id)
            if is_player(current_user,this_game):
                this_user_group = "game-" + url_id + "-" + str(current_user)
            self.send({
                'type': 'websocket.accept'
            })

        async_to_sync(self.channel_layer.group_discard)(
            this_user_group,
            self.channel_name
        )

    def game_update(self, event):
        self.send({
            'type': 'websocket.send',
            'text': str(event['content']),
        })



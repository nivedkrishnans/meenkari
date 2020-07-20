from django.conf import settings
from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer
from .models import *
from .assets import *

game_id="randomegameid"




class HostConsumer(SyncConsumer):

    def websocket_connect(self, event):
        this_user_group = "denied"
        current_user = self.scope["user"]
        url_id =  self.scope["url_route"]["kwargs"]["url_id"]
        print("wuhahahhahaha" + url_id)
        #url_id = self.scope["url_id"]
        if current_user.is_authenticated:
            this_game = Game.objects.get(unite_id=url_id)
            if is_host(current_user,this_game):
                this_user_group = "unite-" + url_id + "-host"
                print('consumer ' + this_user_group)
            else:
                this_user_group = "unite-" + url_id + "-queue"
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
            this_game = Game.objects.get(unite_id=url_id)
            if is_host(current_user,this_game):
                this_user_group = "unite-" + url_id + "-host"
            else:
                this_user_group = "unite-" + url_id + "-queue"
            self.send({
                'type': 'websocket.accept'
            })

        async_to_sync(self.channel_layer.group_discard)(
            this_user_group,
            self.channel_name
        )

    def queue_update(self, event):
        self.send({
            'type': 'websocket.send',
            'text': str(event['content']),
        })





#test and trials
class LiveConsumer(SyncConsumer):

    def websocket_connect(self, event):
        this_user_group = "denied"
        current_user = self.scope["user"]
        if current_user.is_authenticated:
            this_user_group = game_id + '-' + current_user.username

        self.send({
            'type': 'websocket.accept'
        })

        # Join ticks group
        async_to_sync(self.channel_layer.group_add)(
            this_user_group,
            self.channel_name
        )

    def websocket_disconnect(self, event):
        this_user_group = "denied"
        current_user = self.scope["user"]
        if current_user.is_authenticated:
            this_user_group = game_id + '-' + current_user.username

        async_to_sync(self.channel_layer.group_discard)(
            this_user_group,
            self.channel_name
        )

    def game_update(self, event):
        self.send({
            'type': 'websocket.send',
            'text': self.scope["user"].username + str(event['content']),
        })
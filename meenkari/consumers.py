from django.conf import settings
from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer

game_id="randomegameid"

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

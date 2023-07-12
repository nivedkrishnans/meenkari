from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import *
from .assets import *

game_id=""

class LobbyConsumer(WebsocketConsumer):
    def connect(self):
        # Adding the user to the appropriate group
        current_user = self.scope["user"]
        url_id =  self.scope["url_route"]["kwargs"]["url_id"]
        if current_user.is_authenticated:
            group = lobby_group_name(current_user,url_id)
            async_to_sync(self.channel_layer.group_add)(
                group, self.channel_name
            )      
            self.accept()
            async_to_sync(self.channel_layer.group_send)(
                group, {"type": "confirmation_message", "message": "Jello from the server (LobbyConsumer >> connect)"}
            )
        else:
            self.close()

    def disconnect(self, close_code):
        current_user = self.scope["user"]
        url_id =  self.scope["url_route"]["kwargs"]["url_id"]
        if current_user.is_authenticated:
            group = lobby_group_name(current_user,url_id)
            # Leave room group
            async_to_sync(self.channel_layer.group_discard)(
                group, self.channel_name
            )

    # Receive message from WebSocket
    def receive(self, text_data):
        print("hi")
        current_user = self.scope["user"]
        url_id =  self.scope["url_route"]["kwargs"]["url_id"]
        group = lobby_group_name(current_user,url_id)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            group, {"type": "confirmation_message", "message": json.loads(text_data)["message"]}
        )
    # Receive message from room group
    def confirmation_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))

    def lobby_update(self, event):
        self.send(text_data = str(event['content']))


class GameConsumer(WebsocketConsumer):
    def connect(self):
        # Adding the user to the appropriate group
        current_user = self.scope["user"]
        url_id =  self.scope["url_route"]["kwargs"]["url_id"]
        if current_user.is_authenticated:
            group = game_group_name(current_user,url_id)
            async_to_sync(self.channel_layer.group_add)(
                group, self.channel_name
            )      
            self.accept()
            self.send(text_data=json.dumps({"message": "Hello from the server"}))
        else:
            self.close()

    def disconnect(self, close_code):
        group = "denied"
        current_user = self.scope["user"]
        url_id =  self.scope["url_route"]["kwargs"]["url_id"]
        if current_user.is_authenticated:
            group = game_group_name(current_user,url_id)
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            group, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        current_user = self.scope["user"]
        url_id =  self.scope["url_route"]["kwargs"]["url_id"]
        group = lobby_group_name(current_user,url_id)
        # Send message to room group
        # We avoid this because the game page assumes all messages from the server to be a game update so will end up throwing an erro
        # async_to_sync(self.channel_layer.group_send)(
        #     group, {"type": "confirmation_message", "message": json.loads(text_data)["message"]}
        # )
    # Receive message from room group
    def confirmation_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))

    def game_update(self, event):
        self.send(text_data = str(event['content']))


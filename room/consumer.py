import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer  # type: ignore


class RoomConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        async_to_sync(self.channel_layer.group_add)(
            "components_group",
            self.channel_name,
        )

        async_to_sync(self.channel_layer.group_add)(
            "rooms_group",
            self.channel_name,
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            "components_group",
            self.channel_name,
        )

        async_to_sync(self.channel_layer.group_discard)(
            "rooms_group",
            self.channel_name,
        )
        pass

    def receive(self, text_data):
        # Lógica para receber mensagens via WebSocket
        pass

    def send_rooms_updated(self, event):
        self.send(
            text_data=json.dumps(
                {
                    "type": "rooms_updated",
                    "message": "As salas foram alteradas.",
                }
            )
        )

    def send_components_updated(self, event):
        self.send(
            text_data=json.dumps(
                {
                    "type": "components_updated",
                    "message": "Os componentes foram alterados.",
                }
            )
        )

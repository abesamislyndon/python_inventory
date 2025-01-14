import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ClientMsg, Client

class MessageBoardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract client_url from the URL route
        self.client_url = self.scope['url_route']['kwargs']['client_url']
        self.group_name = f"message_board_{self.client_url}"

        # Add the WebSocket connection to the group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Remove the WebSocket connection from the group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        guest_name = data["guest_name"]
        client_id = data["client_id"]
        content = data["content"]

        # Save the message to the database
        try:
            client = Client.objects.get(id=client_id)
            new_message = ClientMsg.objects.create(
                guest_name=guest_name,
                client=client,
                content=content,
            )

            # Broadcast the message to the group
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "new_message",
                    "guest_name": new_message.guest_name,
                    "client_name": client.name,
                    "content": new_message.content,
                    "created_at": new_message.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "image_url": new_message.image.url if new_message.image else None,
                },
            )
        except Client.DoesNotExist:
            # Handle case where client doesn't exist
            await self.send(text_data=json.dumps({"error": "Client not found"}))

    async def new_message(self, event):
        # Send the broadcast message to the WebSocket
        await self.send(text_data=json.dumps(event))

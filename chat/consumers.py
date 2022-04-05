# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chat.models import Room


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        has_room = await self.has_room(self.room_name)
        if has_room:
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.delete_room(self.scope['url_route']['kwargs']['room_name'])
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_uuid = text_data_json['user_uuid']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user_uuid': user_uuid
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user_uuid': event['user_uuid']
        }))

    @database_sync_to_async
    def delete_room(self, name):
        try:
            Room.objects.get(name=name).delete()
        except Room.DoesNotExist:
            pass

    @database_sync_to_async
    def has_room(self, name):
        return Room.objects.filter(name=name).exists()

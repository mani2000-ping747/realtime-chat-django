import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()
online_users = {}


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)

        if "typing" in data:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "typing_status",
                    "typing": data["typing"],
                    "username": data["username"],
                },
            )

        elif "message" in data:
            await self.save_message(data["username"], self.room_name, data["message"])
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": data["message"],
                    "username": data["username"],
                },
            )

        elif "file_url" in data:
            await self.save_message(
                data["username"], self.room_name, "", data["file_url"]
            )
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "file_message",
                    "file_url": data["file_url"],
                    "username": data["username"],
                },
            )

    async def file_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "file_url": event["file_url"],
                    "username": event["username"],
                }
            )
        )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "message": event["message"],
                    "username": event["username"],
                }
            )
        )

    async def typing_status(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "typing": event["typing"],
                    "username": event["username"],
                }
            )
        )

    async def online_users(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "users": event["users"],
                }
            )
        )

    @database_sync_to_async
    def save_message(self, username, room_name, message, file_url=None):
        user = User.objects.get(username=username)
        msg = Message(user=user, room_name=room_name, content=message)
        if file_url:
            msg.file.name = file_url
        msg.save()

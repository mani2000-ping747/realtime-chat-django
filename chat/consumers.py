# # import json
# # from channels.generic.websocket import AsyncWebsocketConsumer
# # from channels.db import database_sync_to_async
# # from .models import Message
# # from django.contrib.auth import get_user_model

# # User = get_user_model()
# # online_users = {}


# # class ChatConsumer(AsyncWebsocketConsumer):
# #     async def connect(self):
# #         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
# #         self.room_group_name = f"chat_{self.room_name}"

# #         await self.channel_layer.group_add(self.room_group_name, self.channel_name)
# #         await self.accept()

# #     async def disconnect(self, close_code):
# #         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

# #     async def receive(self, text_data):
# #         data = json.loads(text_data)

# #         if "typing" in data:
# #             await self.channel_layer.group_send(
# #                 self.room_group_name,
# #                 {
# #                     "type": "typing_status",
# #                     "typing": data["typing"],
# #                     "username": data["username"],
# #                 },
# #             )

# #         elif "message" in data:
# #             await self.save_message(data["username"], self.room_name, data["message"])
# #             await self.channel_layer.group_send(
# #                 self.room_group_name,
# #                 {
# #                     "type": "chat_message",
# #                     "message": data["message"],
# #                     "username": data["username"],
# #                 },
# #             )

# #         elif "file_url" in data:
# #             await self.save_message(
# #                 data["username"], self.room_name, "", data["file_url"]
# #             )
# #             await self.channel_layer.group_send(
# #                 self.room_group_name,
# #                 {
# #                     "type": "file_message",
# #                     "file_url": data["file_url"],
# #                     "username": data["username"],
# #                 },
# #             )

# #     async def file_message(self, event):
# #         await self.send(
# #             text_data=json.dumps(
# #                 {
# #                     "file_url": event["file_url"],
# #                     "username": event["username"],
# #                 }
# #             )
# #         )

# #     async def chat_message(self, event):
# #         await self.send(
# #             text_data=json.dumps(
# #                 {
# #                     "message": event["message"],
# #                     "username": event["username"],
# #                 }
# #             )
# #         )

# #     async def typing_status(self, event):
# #         await self.send(
# #             text_data=json.dumps(
# #                 {
# #                     "typing": event["typing"],
# #                     "username": event["username"],
# #                 }
# #             )
# #         )

# #     async def online_users(self, event):
# #         await self.send(
# #             text_data=json.dumps(
# #                 {
# #                     "users": event["users"],
# #                 }
# #             )
# #         )

# #     async def gif_message(self, event):
# #         await self.send(
# #             json.dumps(
# #                 {
# #                     "gif_url": event["gif_url"],
# #                     "username": event["username"],
# #                 }
# #             )
# #         )

# #     @database_sync_to_async
# #     def save_message(self, username, room_name, message, file_url=None):
# #         user = User.objects.get(username=username)
# #         msg = Message(user=user, room_name=room_name, content=message)
# #         if file_url:
# #             msg.file.name = file_url
# #         msg.save()

# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from .models import Message
# from django.contrib.auth import get_user_model

# User = get_user_model()
# online_users = {}


# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         self.room_group_name = f"chat_{self.room_name}"

#         await self.channel_layer.group_add(self.room_group_name, self.channel_name)
#         await self.accept()

#         # Send previous messages after connecting
#         previous_messages = await self.get_previous_messages(self.room_name)
#         await self.send(text_data=json.dumps({"previous_messages": previous_messages}))

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

#     async def receive(self, text_data):
#         data = json.loads(text_data)

#         if "typing" in data:
#             await self.channel_layer.group_send(
#                 self.room_group_name,
#                 {
#                     "type": "typing_status",
#                     "typing": data["typing"],
#                     "username": data["username"],
#                 },
#             )

#         elif "message" in data:
#             await self.save_message(data["username"], self.room_name, data["message"])
#             await self.channel_layer.group_send(
#                 self.room_group_name,
#                 {
#                     "type": "chat_message",
#                     "message": data["message"],
#                     "username": data["username"],
#                 },
#             )

#         elif "file_url" in data:
#             await self.save_message(
#                 data["username"], self.room_name, "", data["file_url"]
#             )
#             await self.channel_layer.group_send(
#                 self.room_group_name,
#                 {
#                     "type": "file_message",
#                     "file_url": data["file_url"],
#                     "username": data["username"],
#                 },
#             )

#     async def file_message(self, event):
#         await self.send(
#             text_data=json.dumps(
#                 {
#                     "file_url": event["file_url"],
#                     "username": event["username"],
#                 }
#             )
#         )

#     async def chat_message(self, event):
#         await self.send(
#             text_data=json.dumps(
#                 {
#                     "message": event["message"],
#                     "username": event["username"],
#                 }
#             )
#         )

#     async def typing_status(self, event):
#         await self.send(
#             text_data=json.dumps(
#                 {
#                     "typing": event["typing"],
#                     "username": event["username"],
#                 }
#             )
#         )

#     async def online_users(self, event):
#         await self.send(
#             text_data=json.dumps(
#                 {
#                     "users": event["users"],
#                 }
#             )
#         )

#     async def gif_message(self, event):
#         await self.send(
#             json.dumps(
#                 {
#                     "gif_url": event["gif_url"],
#                     "username": event["username"],
#                 }
#             )
#         )

#     @database_sync_to_async
#     def save_message(self, username, room_name, message, file_url=None):
#         user = User.objects.get(username=username)
#         msg = Message(user=user, room_name=room_name, content=message)
#         if file_url:
#             msg.file.name = file_url
#         msg.save()

#     @database_sync_to_async
#     def get_previous_messages(self, room_name):
#         messages = Message.objects.filter(room_name=room_name).order_by("timestamp")[
#             :50
#         ]
#         return [
#             {
#                 "username": msg.user.username,
#                 "message": msg.content,
#                 "file_url": msg.file.url if msg.file else None,
#                 "timestamp": msg.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
#             }
#             for msg in messages
#         ]


import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Message
from django.utils.timezone import localtime

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Send last 50 messages
        previous_messages = await self.get_previous_messages(self.room_name)
        await self.send(text_data=json.dumps({"previous_messages": previous_messages}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        user = self.scope["user"]

        if "typing" in data:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "typing_status",
                    "typing": data["typing"],
                    "username": user.username,
                },
            )

        elif "message" in data:
            message = data["message"]
            await self.save_message(
                user=user, room_name=self.room_name, message=message
            )

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "username": user.username,
                },
            )

        elif "file_url" in data:
            file_url = data["file_url"]
            file_heading = data.get("file_heading", "")
            gif_url = data.get("gif_url", None)
            is_sticker = data.get("is_sticker", False)

            await self.save_message(
                user=user,
                room_name=self.room_name,
                message="",
                file_url=file_url,
                file_heading=file_heading,
                gif_url=gif_url,
                is_sticker=is_sticker,
            )

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "file_message",
                    "file_url": file_url,
                    "file_heading": file_heading,
                    "gif_url": gif_url,
                    "is_sticker": is_sticker,
                    "username": user.username,
                },
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

    async def file_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "file_url": event["file_url"],
                    "file_heading": event.get("file_heading"),
                    "gif_url": event.get("gif_url"),
                    "is_sticker": event.get("is_sticker", False),
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

    @database_sync_to_async
    def save_message(
        self,
        user,
        room_name,
        message="",
        file_url=None,
        file_heading="",
        gif_url=None,
        is_sticker=False,
    ):
        file_field = None
        if file_url:
            # Simulate FileField path only if saving file as a URL (not actual upload)
            from django.core.files.base import ContentFile
            import os

            name = os.path.basename(file_url)
            file_field = ContentFile(b"", name=name)  # Empty placeholder file
        return Message.objects.create(
            user=user,
            room_name=room_name,
            content=message,
            file_heading=file_heading,
            file=file_field,
            gif_url=gif_url,
            is_sticker=is_sticker,
        )

    @database_sync_to_async
    def get_previous_messages(self, room_name):
        messages = Message.objects.filter(room_name=room_name).order_by("timestamp")
        return [
            {
                "username": msg.user.username,
                "message": msg.content,
                "file_url": msg.file.url if msg.file else None,
                "file_heading": msg.file_heading,
                "gif_url": msg.gif_url,
                "is_sticker": msg.is_sticker,
                "timestamp": localtime(msg.timestamp).strftime("%Y-%m-%d %H:%M:%S"),
            }
            for msg in messages
        ]

import json
from asgiref.sync import sync_to_async

from .models import AIChatLog
from .constants import CHAT_CONTENT, INIT_CONTENT
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.exceptions import ObjectDoesNotExist

from openai import AsyncOpenAI
from config.settings import OPENAI_API_KEY

client = AsyncOpenAI(api_key=OPENAI_API_KEY)


class ChatBotConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        user = self.scope["user"]
        try:
            chatlog = await AIChatLog.objects.aget(user=user)
            self.messages = chatlog.messages
        except ObjectDoesNotExist:
            init_messages = [
                {
                    "role": "system",
                    "content": INIT_CONTENT,
                },
            ]
            scenario = await self.get_bot_response(init_messages)
            self.messages = [
                {
                    "role": "system",
                    "content": CHAT_CONTENT.format("B1", user.nickname, scenario),
                },
            ]
        bot_res = await self.get_bot_response(self.messages)
        self.messages.append(
            {
                "role": bot_res.role,
                "content": bot_res.content,
            }
        )
        await self.send(
            text_data=json.dumps(
                {
                    "role": bot_res.role,
                    "content": bot_res.content,
                }
            )
        )

    async def disconnect(self, close_code):
        user = self.scope["user"]
        chatlog = await AIChatLog.objects.aget_or_create(
            user=user, defaults={"messages": self.messages}
        )

    async def receive(self, text_data):
        user_res = json.loads(text_data)
        self.messages.append(
            {
                "role": user_res["role"],
                "content": user_res["content"],
            }
        )
        bot_res = await self.get_bot_response(self.messages)
        self.messages.append(
            {
                "role": bot_res.role,
                "content": bot_res.content,
            }
        )

        await self.send(
            text_data=json.dumps(
                {
                    "role": bot_res.role,
                    "content": bot_res.content,
                }
            )
        )

    @classmethod
    async def get_bot_response(cls, messages):
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
        return response.choices[0].message


# class ChatUserConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         print(self.scope)
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         self.room_group_name = f"chat_{self.room_name}"

#         # Join room group
#         await self.channel_layer.group_add(self.room_group_name, self.channel_name)

#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]
#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name, {"type": "chat.message", "message": message}
#         )

#     # Receive message from room group
#     async def chat_message(self, event):
#         message = event["message"]

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({"message": message}))

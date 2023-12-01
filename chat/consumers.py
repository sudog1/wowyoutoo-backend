import json
from asgiref.sync import sync_to_async

from .models import AIChatLog
from .constants import CHAT_COST, CONTENT
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.exceptions import ObjectDoesNotExist

from openai import AsyncOpenAI
from config.settings import DEEPL_API_KEY, OPENAI_API_KEY
import deepl

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

translator = deepl.Translator(DEEPL_API_KEY)


class ChatBotConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        user = self.scope["user"]
        # 채팅을 가져오거나 생성
        chatlog_tuple = await AIChatLog.objects.aget_or_create(user=user)
        self.chatlog = chatlog_tuple[0]
        # 채팅 진행중
        if self.chatlog.ongoing:
            messages = self.chatlog.messages
        # 채팅 첫 시작 또는 재시작
        else:
            if user.coin >= CHAT_COST:
                user.coin -= CHAT_COST
                user.save()
            else:
                self.close(5000)
            # 새로운 대화 시작
            messages = [
                {
                    "role": "system",
                    "content": CONTENT.format(nickname=user.nickname),
                },
            ]
            self.chatlog.ongoing = True
            self.chatlog.messages = messages
        # 대화를 처음 시작하거나 마지막에 유저가 답한 경우
        if messages[-1]["role"] != "assistant":
            bot_res = await ChatBotConsumer.get_bot_response(messages)
            messages.append(
                {
                    "role": bot_res.role,
                    "content": bot_res.content,
                }
            )
        await self.send(text_data=json.dumps(messages[1:]))

    async def disconnect(self, close_code):
        if close_code == 1000:
            self.chatlog.ongoing = False
        await self.chatlog.asave()

    async def receive(self, text_data):
        messages = self.chatlog.messages
        user_res = json.loads(text_data)
        messages.append(
            {
                "role": user_res["role"],
                "content": user_res["content"],
            }
        )
        bot_res = await ChatBotConsumer.get_bot_response(messages)
        messages.append(
            {
                "role": bot_res.role,
                "content": bot_res.content,
            }
        )
        await self.send(
            text_data=json.dumps(
                [
                    {
                        "role": bot_res.role,
                        "content": bot_res.content,
                    }
                ]
            )
        )

    @classmethod
    async def get_bot_response(cls, messages):
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
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

import json
from asgiref.sync import sync_to_async

from .models import AIChatLog
from .constants import CHAT_CONTENT, INIT_CONTENT
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.exceptions import ObjectDoesNotExist

from openai import AsyncOpenAI
from config.settings import OPENAI_API_KEY
from collections import deque

client = AsyncOpenAI(api_key=OPENAI_API_KEY)


class ChatBotConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        await self.accept()
        # 채팅을 가져오거나 생성
        self.chatlog = await AIChatLog.objects.aget_or_create(user=user)
        # 채팅 진행중
        if self.chatlog.ongoing:
            scenario = self.chatlog.scenario
            messages = self.chatlog.messages
            # token_count = self.chatlog.token_count
        # 채팅 첫 시작 또는 재시작
        else:
            # 새로운 시나리오 생성
            init_messages = [
                {
                    "role": "system",
                    "content": INIT_CONTENT,
                },
            ]
            scenario = await ChatBotConsumer.create_scenario(init_messages)
            # 시스템 메시지 추가
            messages = [
                {
                    "role": "system",
                    "content": CHAT_CONTENT.format(user.nickname, "B1", scenario),
                },
            ]
            self.chatlog.ongoing = True
            self.chatlog.scenario = scenario
            self.chatlog.messags = messages

        # 대화를 시작했거나 마지막에 유저가 답한 경우
        if messages[-1]["role"] != "assistant":
            bot_res = await ChatBotConsumer.get_bot_response(messages)
            messages.append(
                {
                    "role": bot_res.role,
                    "content": bot_res.content,
                }
            )
        await self.send(
            text_data=json.dumps({"scenario": scenario, "messages": messages})
        )

    async def disconnect(self, close_code):
        self.chatlog.save()

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
            temperature=0.7,
        )
        return response.choices[0].message

    @classmethod
    async def create_scenario(cls, messages):
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={"type": "json_object"},
            messages=messages,
            temperature=1,
        )
        return response.choices[0].message.content


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

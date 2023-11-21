import json
import g4f as openai
from asgiref.sync import sync_to_async
from .constants import content
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatBotConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.messages = [
            {"role": "system", "content": content},
        ]
        bot_msg = await self.get_bot_answer(self.messages)
        self.messages.append({"role": "assistant", "content": bot_msg})

        await self.accept()
        await self.send(
            text_data=json.dumps(
                {
                    "message": bot_msg,
                }
            )
        )

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        user_msg = json.loads(text_data).get("message")
        self.messages.append({"role": "user", "content": user_msg})
        bot_msg = await self.get_bot_answer(self.messages)
        self.messages.append({"role": "assistant", "content": bot_msg})

        await self.send(
            text_data=json.dumps(
                {
                    "message": bot_msg,
                }
            )
        )

    @classmethod
    @sync_to_async
    def get_bot_answer(cls, messages):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=2,
            finish_reason="length",
            # stream=True,
        )
        return response


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

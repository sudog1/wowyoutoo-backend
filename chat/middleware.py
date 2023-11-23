from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken


class WebSocketAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        params = parse_qs(query_string)
        access_token = params.get("access")[0]
        token = AccessToken(access_token)
        user = await self.authenticate_user(token)
        if user is None:
            await self.deny_access(send)
            return

        scope["user"] = user
        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def authenticate_user(self, token):
        try:
            auth_user = JWTAuthentication().get_user(token)
            return auth_user
        except Exception as e:
            return None

    async def deny_access(self, send):
        await send({"type": "websocket.close", "code": 403})

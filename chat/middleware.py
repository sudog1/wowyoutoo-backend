from urllib.parse import parse_qs
from dj_rest_auth.models import TokenModel
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from rest_framework_simplejwt.authentication import JWTAuthentication


class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        scope = dict(scope)
        query_string = scope.get("query_string", b"").decode()
        params = parse_qs(query_string)

        access_token = params.get("access")

        if access_token:
            user = self.get_user(access_token[0])

            if user:
                scope["user"] = user

        return await self.inner(scope, receive, send)

    @database_sync_to_async
    def get_user(self, token):
        try:
            user = TokenModel.objects.get(key=token).user
        except:
            user = AnonymousUser()
        return user


class WebSocketAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        params = parse_qs(query_string)
        token = params.get("access")
        user = await self.authenticate_user(token)
        if user is None:
            await self.deny_access(send)
            return

        scope["user"] = user
        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def authenticate_user(self, token):
        try:
            jwt_auth = JWTAuthentication()
            # validated_token = jwt_auth.get_validated_token(token)
            print(token)
            auth_user = jwt_auth.get_user(token)
            return auth_user
        except Exception as e:
            return None

    async def deny_access(self, send):
        await send({"type": "websocket.close", "code": 403})

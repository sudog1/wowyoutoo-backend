from urllib.parse import parse_qs
from dj_rest_auth.models import TokenModel
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser


class TokenAuthMiddleware:
    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        params = parse_qs(query_string)

        access_token = params.get("access")

        if access_token:
            user = self.authenticate(access_token[0])

            if user:
                scope["user"] = user

        return await self.inner(scope, receive, send)

    def __init__(self, inner):
        self.inner = inner

    @database_sync_to_async
    def authenticate(self, token):
        try:
            user = TokenModel.objects.get(key=token).user
        except:
            user = AnonymousUser()
        return user

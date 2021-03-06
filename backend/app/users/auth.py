from channels.auth import AuthMiddlewareStack
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections

from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

from rest_framework.authtoken.models import Token

@database_sync_to_async
def get_user_from_token(headers):
    try:
        token_name, token_key = headers[b'authorization'].decode().split()
        if token_name == 'Token':
            token = Token.objects.get(key=token_key)
            return token.user
    except Token.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        if b'authorization' in headers:
            scope['user'] = await get_user_from_token(headers)
        try:
            x = await self.inner(scope, receive, send)
            print(x)
        except Exception as e:
            print(e)
        return x


# class TokenAuthMiddlewareInstance:
#     def __init__(self, scope, middleware):
#         self.middleware = middleware
#         self.scope = dict(scope)
#         self.inner = self.middleware.inner

#     async def __call__(self, receive, send):
#         headers = dict(self.scope['headers'])
#         if b'authorization' in headers:
#             self.scope['user'] = await get_user_from_token(headers)
#         inner = self.inner(self.scope)
#         return await inner(receive, send)

def TokenAuthMiddlewareStack(inner): 
    return TokenAuthMiddleware(AuthMiddlewareStack(inner))    

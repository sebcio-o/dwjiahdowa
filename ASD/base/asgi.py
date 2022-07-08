"""
ASGI config for base project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os


from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application

from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

import root.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')

application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": application,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                root.routing.websocket_urlpatterns
            )
        )
    )
})

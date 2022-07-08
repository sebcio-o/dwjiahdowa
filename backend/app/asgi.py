import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from users.auth import TokenAuthMiddlewareStack

from django.urls import path

from routing import urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings.local")

django_app = get_asgi_application()


application = ProtocolTypeRouter({
    "http": django_app,
    'websocket': TokenAuthMiddlewareStack(
        URLRouter([
            path("ws/", urlpatterns)
        ])
    )
})
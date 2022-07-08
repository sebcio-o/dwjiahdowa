from django.urls import path
from channels.routing import URLRouter
from app.watcher.consumers import WatcherConsumer

urlpatterns = URLRouter([
    path("", WatcherConsumer.as_asgi())
])
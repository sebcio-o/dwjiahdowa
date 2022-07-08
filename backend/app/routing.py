from django.urls import path

from channels.routing import URLRouter

from app.watcher.routing import urlpatterns as watcher_urlpatterns  

urlpatterns = URLRouter([
    path("watcher/", watcher_urlpatterns)
])
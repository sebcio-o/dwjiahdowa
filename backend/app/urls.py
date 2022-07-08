from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/cards/", include("cards.urls")),
    path("api/lists/", include("lists.urls")),
    path("api/boards/", include("boards.urls")),
    path("api/workspaces/", include("workspaces.urls")),
    path("api/cards/", include("cards.urls")),
    path("api/auth/", include("djoser.urls")),
    path("api/auth/", include("djoser.urls.authtoken")),
    path("api/admin/", admin.site.urls),
]

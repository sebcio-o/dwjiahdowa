from app.workspaces.views import (
    WorkspaceInvitationGetAccessView,
    WorkspaceInvitationViewSet,
    WorkspacePermissionViewSet,
    WorkspaceViewSet,
)
from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

router = SimpleRouter()
router.register("", WorkspaceViewSet, basename="workspace")

workspace_router = routers.NestedSimpleRouter(router, "", lookup="workspace")
workspace_router.register("invite", WorkspaceInvitationViewSet, basename="invite")
workspace_router.register(
    "permissions", WorkspacePermissionViewSet, basename="permissions"
)


urlpatterns = [
    path("", include(router.urls)),
    path("", include(workspace_router.urls)),
    path("access/<str:token>/", WorkspaceInvitationGetAccessView.as_view()),
]

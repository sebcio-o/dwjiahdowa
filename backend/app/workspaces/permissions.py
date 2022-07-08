from app.workspaces.models import WorkspacePermission
from rest_framework.permissions import  IsAuthenticated
from app.workspaces.helpers import get_user2workspace_permission


class IsWorkspaceAdministrator(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        user2workspace_permission = get_user2workspace_permission(obj, request.user)
        if not user2workspace_permission:
            return False

        return (
            user2workspace_permission.access_type
            == WorkspacePermission.AccessTypes.ADMINISTRATOR
        )


class IsWorkspaceAdministratorOnNestedViewset(IsAuthenticated):
    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        if not is_authenticated:
            return False

        workspace_pk = view.kwargs.get("workspace_pk", "")
        if not workspace_pk.isdigit():
            return False

        user2workspace_permission = get_user2workspace_permission(int(workspace_pk), request.user)
        if not user2workspace_permission:
            return False
            
        return (
            user2workspace_permission.access_type
            == WorkspacePermission.AccessTypes.ADMINISTRATOR
        )

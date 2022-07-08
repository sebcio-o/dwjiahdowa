from rest_framework.permissions import  BasePermission
from app.workspaces.models import WorkspacePermission
from app.boards.models import Board
from app.workspaces.helpers import get_user2workspace_permission

from app.utils import extract_workspace_from_obj

import abc

class IsBoardXType(abc.ABC):
    @property
    @abc.abstractmethod
    def access_types(self, access_type): WorkspacePermission.AccessTypes.choices

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
        
    def has_object_permission(self, request, view, obj):
        workspace = extract_workspace_from_obj(obj)
        if not workspace:
            return False

        user2workspace_permission = get_user2workspace_permission(workspace, request.user)
        if not user2workspace_permission:
            return False

        return (
            user2workspace_permission.access_type
            in self.access_types
        )

class IsBoardAdmin(IsBoardXType):
    access_types = [WorkspacePermission.AccessTypes.ADMINISTRATOR]

class IsBoardNormalUser(IsBoardXType):
    access_types = [WorkspacePermission.AccessTypes.NORMAL, WorkspacePermission.AccessTypes.ADMINISTRATOR]

class CanViewBoard(BasePermission):
    def has_object_permission(self, request, view, obj):
        workspace = extract_workspace_from_obj(obj)

        if obj.access_level == Board.AccessLevels.PUBLIC:
            return True
        if not request.user.is_authenticated:
            return False

        user2workspace_permission = get_user2workspace_permission(workspace, request.user)
        if not user2workspace_permission:
            return False

        return True

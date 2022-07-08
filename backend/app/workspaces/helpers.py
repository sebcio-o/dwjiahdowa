from typing import Optional
from app.workspaces.models import WorkspacePermission

def get_user2workspace_permission(workspace, user) -> Optional[WorkspacePermission]:
    try:
        return WorkspacePermission.objects.get(
            workspace=workspace, user=user
        )
    except WorkspacePermission.DoesNotExist:
        return None

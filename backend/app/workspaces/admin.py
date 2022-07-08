from app.workspaces.models import Workspace, WorkspaceInvitation, WorkspacePermission
from django.contrib import admin

admin.site.register([Workspace, WorkspacePermission, WorkspaceInvitation])

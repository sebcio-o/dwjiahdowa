from app.workspaces.models import Workspace, WorkspaceInvitation, WorkspacePermission
from app.workspaces.permissions import (
    IsWorkspaceAdministrator,
    IsWorkspaceAdministratorOnNestedViewset,
)
from app.workspaces.serializers import (
    WorkspaceInvitationSerializer,
    WorkspacePermissionSerializer,
    WorkspaceSerializer,
)
from django.db import IntegrityError
from django.db.models import F
from rest_framework import generics, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class WorkspaceViewSet(viewsets.ModelViewSet):
    serializer_class = WorkspaceSerializer
    permission_classes = [IsWorkspaceAdministrator]

    def get_queryset(self):
        user = self.request.user
        workspaces_that_user_can_view = WorkspacePermission.objects.values_list(
            "workspace", flat=True
        ).filter(user=user)

        return (
            Workspace.objects.prefetch_related("board_set")
            .prefetch_related("workspacepermission_set")
            .annotate(access_type=F("workspacepermission__access_type"))
            .filter(id__in=workspaces_that_user_can_view)
        )


class WorkspacePermissionViewSet(
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = WorkspacePermissionSerializer
    permission_classes = [IsWorkspaceAdministratorOnNestedViewset]

    def perform_destroy(self, serializer):
        if (
            WorkspacePermission.objects.filter(workspace=serializer.workspace).count()
            == 1
        ):
            raise ValidationError({"detail": "Workspace should have at least one user"})
        return super().perform_destroy(serializer)

    def get_queryset(self):
        workspace_pk = self.kwargs["workspace_pk"]
        return WorkspacePermission.objects.filter(workspace=int(workspace_pk))


class WorkspaceInvitationViewSet(viewsets.ModelViewSet):
    serializer_class = WorkspaceInvitationSerializer
    permission_classes = [IsWorkspaceAdministratorOnNestedViewset]

    def get_queryset(self):
        workspace_pk = self.kwargs["workspace_pk"]
        return WorkspaceInvitation.objects.filter(workspace=int(workspace_pk))


class WorkspaceInvitationGetAccessView(generics.GenericAPIView):
    queryset = WorkspaceInvitation.objects.all()
    lookup_field = "token"
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        workspace_invitation = self.get_object()

        try:
            WorkspacePermission.objects.create(
                workspace=workspace_invitation.workspace,
                user=request.user,
                access_type=WorkspacePermission.AccessTypes.OBSERVER,
            )
        except IntegrityError:
            raise ValidationError("User already in workspace")

        return Response(status.HTTP_201_CREATED)

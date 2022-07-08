from app.boards.serializers import BoardSerializer
from app.workspaces.models import Workspace, WorkspaceInvitation, WorkspacePermission
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class WorkspaceSerializer(serializers.ModelSerializer):
    boards = BoardSerializer(many=True, read_only=True, source="board_set")

    class Meta:
        model = Workspace
        fields = "__all__"
        read_only_fields = ["id", "last_opened", "last_edited", "created_at"]

    @transaction.atomic
    def create(self, validated_data):
        user = self.context["request"].user

        workspace = super().create(validated_data)
        WorkspacePermission.objects.create(
            workspace=workspace,
            user=user,
            access_type=WorkspacePermission.AccessTypes.ADMINISTRATOR,
        )

        return workspace


class WorkspacePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkspacePermission
        fields = ["user", "access_type"]

    def validate_access_type(self, access_type):
        if access_type != WorkspacePermission.AccessTypes.ADMINISTRATOR:
            admins = WorkspacePermission.objects.values_list("user", flat=True).filter(
                workspace=self.instance.workspace,
                access_type=WorkspacePermission.AccessTypes.ADMINISTRATOR,
            )
            if admins.count() == 1 and self.instance.user.id in admins:
                raise ValidationError("Workspace must have at least one administrator")
        return access_type


class WorkspaceInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkspaceInvitation
        fields = ["token", "generated_at", "generated_by"]
        read_only_fields = ["generated_at", "generated_by"]

    def create(self, validated_data):
        request = self.context["request"]
        workspace_pk = request.parser_context["kwargs"]["workspace_pk"]
        workspace = Workspace.objects.get(pk=workspace_pk)
        validated_data = {
            "generated_by": request.user,
            "workspace": workspace,
            **validated_data,
        }
        return super().create(validated_data)

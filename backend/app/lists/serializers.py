from app.lists.models import List
from rest_framework import serializers


from app.workspaces.models import WorkspacePermission
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class ValidateBoard:
    err = ValidationError(
            "You don't have sufficient permissions on particular workspace"
        )

    def validate_board(self, board, *args, **kwargs):
        user = self.context["request"].user
        workspace = board.workspace

        try:
            user2workspace_permission = WorkspacePermission.objects.get(
                workspace=workspace, user=user
            )
        except WorkspacePermission.DoesNotExist:
            raise self.err

        if (
            user2workspace_permission.access_type
            == WorkspacePermission.AccessTypes.OBSERVER
        ):
            raise self.err

        return board

class ListSerializer(serializers.ModelSerializer, ValidateBoard):
    class Meta:
        model = List
        fields = ['id', 'board', 'position', "name"]


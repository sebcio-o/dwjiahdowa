from app.boards.models import Board, BoardOpenTime
from app.workspaces.models import WorkspacePermission
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from app.cards.serializers import CardSerializer
from app.lists.serializers import ListSerializer

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'name', 'workspace', 'access_level']
        read_only_fields = ["id", "created_at"]

    def validate_workspace(self, workspace):
        err = ValidationError(
            "You don't have sufficient permissions on particular workspace"
        )
        user = self.context["request"].user

        try:
            user2workspace_permission = WorkspacePermission.objects.get(
                workspace=workspace, user=user
            )
        except WorkspacePermission.DoesNotExist:
            raise err

        if (
            user2workspace_permission.access_type
            != WorkspacePermission.AccessTypes.ADMINISTRATOR
        ):
            raise err

        return workspace

    @transaction.atomic
    def create(self, validated_data):
        user = self.context["request"].user

        board = super().create(validated_data)
        BoardOpenTime.objects.create(user=user, board=board)

        return board

class BoardDetailSerializer(serializers.ModelSerializer):

    lists = ListSerializer(many=True, source='list_set')
    cards = CardSerializer(many=True, source='card_set')

    class Meta:
        model = Board
        fields = ['id', 'name', 'workspace', 'access_level', 'lists', 'cards']

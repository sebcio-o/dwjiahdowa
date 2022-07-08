from shutil import register_archive_format
from app.boards.models import Board
from app.boards.serializers import BoardSerializer, BoardDetailSerializer
from app.workspaces.models import WorkspacePermission
from app.boards.permissions import CanViewBoard, IsBoardAdmin
from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["workspace"]
    ordering_fields = ["name"]
    ordering = ["name"]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BoardDetailSerializer
        return BoardSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            return [CanViewBoard()]
        return [IsBoardAdmin()]

    def get_queryset(self):
        user = self.request.user
        boards = Board.objects.none()

        if self.action == 'retrieve':
            boards |= Board.objects.filter(access_level = Board.AccessLevels.PUBLIC)
        if not user.is_authenticated:
            return boards

        workspaces_that_user_have_access = WorkspacePermission.objects.values_list(
            "workspace", flat=True
        ).filter(user=user)
        boards |= Board.objects.filter(workspace__in=workspaces_that_user_have_access)

        return boards

    @action(methods=["GET"], detail=False, url_path="latest")
    def get_last_opened_boards(self, request, *args, **kwargs):
        boards = self.get_queryset()
        latest_boards = (
            boards.prefetch_related("boardopentime_set")
            .annotate(last_time_opened=F("boardopentime__time"))
            .order_by("-last_time_opened")
        )
        return Response(BoardSerializer(latest_boards, many=True).data)


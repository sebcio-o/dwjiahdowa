from app.boards.permissions import IsBoardAdmin, CanViewBoard, IsBoardNormalUser
from app.lists.models import List
from app.lists.serializers import ListSerializer
from rest_framework import viewsets, mixins

class ListViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin ,viewsets.GenericViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer
    permission_classes = [IsBoardNormalUser]
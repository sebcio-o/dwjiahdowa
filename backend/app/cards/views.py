from app.cards.models import Card
from app.cards.serializers import CardSerializer
from rest_framework import viewsets, mixins
from app.boards.permissions import IsBoardNormalUser 

from rest_framework.parsers import JSONParser, MultiPartParser

class CardViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin ,viewsets.GenericViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [IsBoardNormalUser]
    parser_classes = [JSONParser, MultiPartParser]

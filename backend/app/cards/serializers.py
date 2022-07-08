from app.cards.models import Card
from rest_framework import serializers

from app.lists.serializers import ValidateBoard

class CardSerializer(serializers.ModelSerializer, ValidateBoard):
    class Meta:
        model = Card
        fields = [
            "id", "board", 'list', 'position', 
            "name", 'description', 'thumbnail', 
            "last_edited", "created_at",
            ]
        read_only_fields = ["id", "created_at", "last_edited"]
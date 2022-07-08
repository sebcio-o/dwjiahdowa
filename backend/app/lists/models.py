from django.db import models
from app.boards.models import Board

class List(models.Model):
    name = models.CharField(max_length=150)
    board = models.ForeignKey(Board, models.CASCADE)
    position = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["board", "position"], name="unique_board_position"
            )
        ]

from app.boards.models import Board
from app.lists.models import List
from app.cards.storages import StorageAllowingDirectURLSave
from app.users.models import CustomUser
from django.db import models
from django.utils import timezone


class Card(models.Model):
    board = models.ForeignKey(Board, models.CASCADE)
    list = models.ForeignKey(List, models.CASCADE)
    position = models.PositiveIntegerField()

    assigned_users = models.ManyToManyField(CustomUser)

    name = models.CharField(max_length=150)
    description = models.TextField()
    thumbnail = models.ImageField(storage=StorageAllowingDirectURLSave, null=True, blank=True)

    last_edited = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["board", "list", "position"], name="unique_list_position"
            )
        ]


class Attachment(models.Model):
    card = models.ForeignKey(Card, models.CASCADE)
    name = models.CharField(max_length=150, null=True, blank=True)
    file = models.FileField(storage=StorageAllowingDirectURLSave)


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, models.CASCADE)
    card = models.ForeignKey(Card, models.CASCADE)
    text = models.TextField()

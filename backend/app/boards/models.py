from app.users.models import CustomUser
from app.workspaces.models import Workspace
from django.db import models
from django.utils.translation import gettext_lazy as _


class Board(models.Model):
    class AccessLevels(models.TextChoices):
        PUBLIC = ("P", _("Public"))
        WORKSPACE = ("W", _("Workspace"))

    name = models.CharField(max_length=150)
    workspace = models.ForeignKey(Workspace, models.CASCADE)
    access_level = models.CharField(
        max_length=1, choices=AccessLevels.choices, default=AccessLevels.WORKSPACE
    )


class BoardOpenTime(models.Model):
    board = models.ForeignKey(Board, models.CASCADE)
    user = models.ForeignKey(CustomUser, models.CASCADE)
    time = models.DateTimeField(_("Last Opened time"), auto_now=True)

    class Meta:
        get_latest_by = "time"
        verbose_name = "last_opened_board"
        constraints = [
            models.UniqueConstraint(
                fields=["board", "user"], name="BoardOpenTime.unique_board_user"
            )
        ]

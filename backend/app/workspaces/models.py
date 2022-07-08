from uuid import uuid4

from app.users.models import CustomUser
from django.db import models
from django.utils.translation import gettext as _


class Workspace(models.Model):
    name = models.CharField(_("Name"), max_length=150)
    last_edited = models.DateTimeField(_("Last edited"), auto_now=True)
    creation_time = models.DateTimeField(_("Creation time"), auto_now_add=True)


class WorkspacePermission(models.Model):
    class AccessTypes(models.TextChoices):
        ADMINISTRATOR = ("A", _("Administrator"))
        NORMAL = ("N", _("Normal"))
        OBSERVER = ("O", _("Observer"))

    workspace = models.ForeignKey(Workspace, models.CASCADE)
    user = models.ForeignKey(CustomUser, models.CASCADE)
    access_type = models.CharField(
        _("Workspace permission type"), max_length=1, choices=AccessTypes.choices
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["workspace", "user"],
                name="WorkspacePermission.unique_workspace_user",
            )
        ]


class WorkspaceInvitation(models.Model):
    token = models.CharField(max_length=255, default=uuid4)
    workspace = models.ForeignKey(Workspace, models.CASCADE)
    generated_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey(CustomUser, models.CASCADE)

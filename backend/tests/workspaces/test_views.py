import pytest
from app.workspaces.models import Workspace, WorkspaceInvitation, WorkspacePermission
from app.workspaces.serializers import (
    WorkspaceInvitationSerializer,
    WorkspacePermissionSerializer,
)
from model_bakery import baker
from rest_framework import status


@pytest.mark.django_db
class TestWorkspace:
    def test_create_workspace_for_user(
        self, client, user_with_token, user2_with_token, workspace
    ):
        workspace_creation_response = client.post(
            "/api/workspaces/", workspace.__dict__
        )
        assert workspace_creation_response.status_code == 201

        r = client.get("/api/workspaces/")
        assert r.status_code == 200
        assert len(r.data) == 1
        assert r.data[0] == workspace_creation_response.data

        workspace = Workspace.objects.get(id=r.data[0]["id"])
        user2workspace_perms = WorkspacePermission.objects.get(
            workspace=workspace, user=user_with_token["user"]
        )
        assert (
            user2workspace_perms.access_type
            == WorkspacePermission.AccessTypes.ADMINISTRATOR
        )

        workspace_as_dict = vars(workspace)
        for field in ["id", "name"]:
            assert workspace_as_dict[field] == r.data[0][field]

        client.set_token(user2_with_token["token"])
        r = client.get("/api/workspaces/")
        assert len(r.data) == 0

    def test_delete_workspace_by_user(self, client, user_with_token, workspace):
        workspace_permission = WorkspacePermission.objects.create(
            workspace=workspace,
            user=user_with_token["user"],
            access_type=WorkspacePermission.AccessTypes.NORMAL,
        )

        r = client.delete(f"/api/workspaces/{workspace.id}/")
        assert r.status_code == status.HTTP_403_FORBIDDEN
        assert r.data == {
            "detail": "You do not have permission to perform this action."
        }

        workspace_permission.access_type = WorkspacePermission.AccessTypes.ADMINISTRATOR
        workspace_permission.save()
        r = client.delete(f"/api/workspaces/{workspace.id}/")
        assert r.status_code == status.HTTP_204_NO_CONTENT

        r = client.get("/api/workspaces/")
        assert r.status_code == status.HTTP_200_OK
        assert len(r.data) == 0
        assert WorkspacePermission.objects.filter(id=workspace.id).count() == 0

    def test_modify_workspace_by_user(self, client, user_with_token, workspace):
        workspace_permission = WorkspacePermission.objects.create(
            workspace=workspace,
            user=user_with_token["user"],
            access_type=WorkspacePermission.AccessTypes.NORMAL,
        )

        r = client.put(f"/api/workspaces/{workspace.id}/", workspace.__dict__)
        assert r.status_code == 403
        assert r.data == {
            "detail": "You do not have permission to perform this action."
        }

        workspace_permission.access_type = WorkspacePermission.AccessTypes.ADMINISTRATOR
        workspace_permission.save()
        workspace.name = "DUPA123"

        r = client.put(f"/api/workspaces/{workspace.id}/", workspace.__dict__)
        assert r.status_code == 200
        assert "DUPA123" == r.data["name"]
        assert "DUPA123" == Workspace.objects.get(id=workspace.id).name

        r = client.get("/api/workspaces/")
        assert r.status_code == 200
        assert len(r.data) == 1
        assert "DUPA123" == r.data[0]["name"]


@pytest.mark.django_db
class TestInvitation:
    def test_list_invitations(self, client, user_with_token, workspace):
        user = user_with_token["user"]
        workspace_permission = WorkspacePermission.objects.create(
            workspace=workspace,
            user=user,
            access_type=WorkspacePermission.AccessTypes.NORMAL,
        )
        workspace_invitation = WorkspaceInvitation.objects.create(
            workspace=workspace, generated_by=user
        )

        r = client.get(f"/api/workspaces/{workspace.id}/invite/")
        assert r.status_code == status.HTTP_403_FORBIDDEN

        workspace_permission.access_type = WorkspacePermission.AccessTypes.ADMINISTRATOR
        workspace_permission.save()

        r = client.get(f"/api/workspaces/{workspace.id}/invite/")
        assert r.status_code == status.HTTP_200_OK
        assert r.data == [WorkspaceInvitationSerializer(workspace_invitation).data]

    def test_create_invitation(self, client, user_with_token, workspace):
        user = user_with_token["user"]
        workspace_permission = WorkspacePermission.objects.create(
            workspace=workspace,
            user=user,
            access_type=WorkspacePermission.AccessTypes.NORMAL,
        )

        r = client.post(f"/api/workspaces/{workspace.id}/invite/")
        assert r.status_code == status.HTTP_403_FORBIDDEN
        assert WorkspaceInvitation.objects.filter(workspace=workspace).count() == 0

        workspace_permission.access_type = WorkspacePermission.AccessTypes.ADMINISTRATOR
        workspace_permission.save()

        r = client.post(f"/api/workspaces/{workspace.id}/invite/")
        workspace_invitations = WorkspaceInvitation.objects.filter(
            workspace=workspace
        ).all()

        assert r.status_code == status.HTTP_201_CREATED
        assert r.data == WorkspaceInvitationSerializer(workspace_invitations[0]).data
        assert workspace_invitations.count() == 1

    def test_delete_invitation(self, client, user_with_token, workspace):
        user = user_with_token["user"]
        workspace_permission = WorkspacePermission.objects.create(
            workspace=workspace,
            user=user,
            access_type=WorkspacePermission.AccessTypes.NORMAL,
        )
        workspace_invitation = WorkspaceInvitation.objects.create(
            workspace=workspace, generated_by=user
        )

        r = client.delete(f"/api/workspaces/asssss/invite/{workspace_invitation.id}/")
        assert r.status_code == status.HTTP_403_FORBIDDEN
        assert WorkspaceInvitation.objects.filter(workspace=workspace).count() == 1

        r = client.delete(
            f"/api/workspaces/{workspace.id}/invite/{workspace_invitation.id}/"
        )
        assert r.status_code == status.HTTP_403_FORBIDDEN
        assert WorkspaceInvitation.objects.filter(workspace=workspace).count() == 1

        workspace_permission.access_type = WorkspacePermission.AccessTypes.ADMINISTRATOR
        workspace_permission.save()

        r = client.delete(
            f"/api/workspaces/{workspace.id}/invite/{workspace_invitation.id}/"
        )
        assert r.status_code == status.HTTP_204_NO_CONTENT
        assert WorkspaceInvitation.objects.filter(workspace=workspace).count() == 0

        r = client.delete(
            f"/api/workspaces/{workspace.id}/invite/{workspace_invitation.id}/"
        )
        assert r.status_code == status.HTTP_404_NOT_FOUND
        assert WorkspaceInvitation.objects.filter(workspace=workspace).count() == 0

    def test_edit_workspace_invitation(self, client, user_with_token, workspace):
        user = user_with_token["user"]
        workspace_invitation = WorkspaceInvitation.objects.create(
            workspace=workspace, generated_by=user
        )

        r = client.put(
            f"/api/workspaces/{workspace.id}/invite/{workspace_invitation.id}/",
            {"token": "DUPA123!"},
        )
        assert r.status_code == status.HTTP_403_FORBIDDEN

        workspace_invitation.token = "DUPA123!"
        workspace_permission = WorkspacePermission.objects.create(
            workspace=workspace,
            user=user,
            access_type=WorkspacePermission.AccessTypes.ADMINISTRATOR,
        )

        r = client.put(
            f"/api/workspaces/{workspace.id}/invite/{workspace_invitation.id}/",
            {"token": "DUPA123!"},
        )
        assert r.status_code == status.HTTP_200_OK
        assert r.data == WorkspaceInvitationSerializer(workspace_invitation).data

        workspace_invitation = WorkspaceInvitation.objects.get(
            id=workspace_invitation.id
        )
        assert workspace_invitation.token == r.data["token"]

    def test_grant_access_to_workspace(self, client, user_with_token, workspace):
        user = user_with_token["user"]
        workspace_invitation = WorkspaceInvitation.objects.create(
            workspace=workspace, generated_by=user
        )

        assert (
            WorkspacePermission.objects.filter(workspace=workspace, user=user).count()
            == 0
        )
        r = client.post(f"/api/workspaces/access/{workspace_invitation.token}/")
        assert r.status_code == status.HTTP_200_OK
        assert WorkspaceInvitation.objects.filter(workspace=workspace).count() == 1

        workspace_permission = WorkspacePermission.objects.get(
            workspace=workspace, user=user
        )
        assert (
            workspace_permission.access_type == WorkspacePermission.AccessTypes.OBSERVER
        )

        r = client.post(f"/api/workspaces/access/{workspace_invitation.token}/")
        assert r.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestWorkspacePermissions:
    def test_list_workspace_permissions(self, client, user, workspace):
        workspace_permission = WorkspacePermission.objects.create(
            workspace=workspace,
            user=user,
            access_type=WorkspacePermission.AccessTypes.NORMAL,
        )

        r = client.get(f"/api/workspaces/{workspace.id}/permissions/")
        assert r.status_code == status.HTTP_403_FORBIDDEN

        workspace_permission.access_type = WorkspacePermission.AccessTypes.ADMINISTRATOR
        workspace_permission.save()

        r = client.get(f"/api/workspaces/{workspace.id}/permissions/")
        assert r.status_code == status.HTTP_200_OK
        assert r.data == [WorkspacePermissionSerializer(workspace_permission).data]

    def test_edit_workspace_permission(self, client, user, user2, workspace):
        workspace_permission = WorkspacePermission.objects.create(
            workspace=workspace,
            user=user,
            access_type=WorkspacePermission.AccessTypes.NORMAL,
        )

        r = client.patch(
            f"/api/workspaces/{workspace.id}/permissions/{workspace_permission.id}/"
        )
        assert r.status_code == status.HTTP_403_FORBIDDEN

        workspace_permission.access_type = WorkspacePermission.AccessTypes.ADMINISTRATOR
        workspace_permission.save()

        r = client.patch(
            f"/api/workspaces/{workspace.id}/permissions/{workspace_permission.id}/",
            {"access_type": WorkspacePermission.AccessTypes.NORMAL},
        )
        assert r.status_code == status.HTTP_400_BAD_REQUEST
        assert r.data == {
            "access_type": ["Workspace must have at least one administrator"]
        }

        workspace_permission2 = WorkspacePermission.objects.create(
            workspace=workspace,
            user=user2,
            access_type=WorkspacePermission.AccessTypes.NORMAL,
        )
        r = client.patch(
            f"/api/workspaces/{workspace.id}/permissions/{workspace_permission2.id}/",
            {"access_type": WorkspacePermission.AccessTypes.OBSERVER},
        )
        workspace_permission2.access_type = WorkspacePermission.AccessTypes.OBSERVER
        assert r.status_code == status.HTTP_200_OK
        assert r.data == WorkspacePermissionSerializer(workspace_permission2).data

    def test_delete_workspace_permission(self, client, user, user2, workspace):
        workspace_permission = WorkspacePermission.objects.create(
            workspace=workspace,
            user=user,
            access_type=WorkspacePermission.AccessTypes.NORMAL,
        )

        r = client.delete(
            f"/api/workspaces/{workspace.id}/permissions/{workspace_permission.id}/"
        )
        assert r.status_code == status.HTTP_403_FORBIDDEN

        workspace_permission.access_type = WorkspacePermission.AccessTypes.ADMINISTRATOR
        workspace_permission.save()

        r = client.delete(
            f"/api/workspaces/{workspace.id}/permissions/{workspace_permission.id}/",
        )
        assert r.status_code == status.HTTP_400_BAD_REQUEST
        assert r.data == {"detail": "Workspace should have at least one user"}

        workspace_permission = WorkspacePermission.objects.create(
            workspace=workspace,
            user=user2,
            access_type=WorkspacePermission.AccessTypes.NORMAL,
        )
        r = client.delete(
            f"/api/workspaces/{workspace.id}/permissions/{workspace_permission.id}/",
        )
        assert r.status_code == status.HTTP_204_NO_CONTENT

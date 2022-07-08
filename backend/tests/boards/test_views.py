import pytest
from app.boards.models import Board, BoardOpenTime
from app.workspaces.models import WorkspacePermission
from rest_framework import status

from app.boards.serializers import BoardSerializer, BoardDetailSerializer

@pytest.mark.django_db
def test_create_board(client, user_with_token, workspace, prepared_board):
    user = user_with_token["user"]

    r = client.post(
        "/api/boards/",
        {
            "workspace": workspace.id,
            "name": prepared_board.name,
            "access_level": Board.AccessLevels.WORKSPACE,
        },
    )
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert r.data == {
        "workspace": ["You don't have sufficient permissions on particular workspace"]
    }

    workspace_permissions = WorkspacePermission(
        workspace=workspace,
        user=user,
        access_type=WorkspacePermission.AccessTypes.NORMAL,
    )
    workspace_permissions.save()

    r = client.post(
        "/api/boards/",
        {
            "workspace": workspace.id,
            "name": prepared_board.name,
            "access_level": Board.AccessLevels.WORKSPACE,
        },
    )
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert r.data == {
        "workspace": ["You don't have sufficient permissions on particular workspace"]
    }

    workspace_permissions.access_type = WorkspacePermission.AccessTypes.ADMINISTRATOR
    workspace_permissions.save()

    r = client.post(
        "/api/boards/",
        {
            "workspace": workspace.id,
            "name": prepared_board.name,
            "access_level": Board.AccessLevels.WORKSPACE,
        },
    )
    assert r.status_code == status.HTTP_201_CREATED
    board = Board.objects.get(id=r.data["id"])
    assert r.data == BoardSerializer(board).data
    assert board.access_level == Board.AccessLevels.WORKSPACE
    assert BoardOpenTime.objects.filter(board=board, user=user).count() == 1

    client.logout()
    r = client.post(
        "/api/boards/",
        {
            "workspace": workspace.id,
            "name": prepared_board.name,
            "access_level": Board.AccessLevels.WORKSPACE,
        },
    )
    assert r.status_code == status.HTTP_401_UNAUTHORIZED



@pytest.mark.django_db
def test_get_board_details_on_workspace_board(client, user, multiple_boards):
    boards_ids = [i.id for i in multiple_boards]

    r1 = client.get(f"/api/boards/{boards_ids[0]}/")
    r2 = client.get(f"/api/boards/{boards_ids[1]}/")
    assert r1.status_code == status.HTTP_200_OK
    assert r2.status_code == status.HTTP_200_OK

    board1_time = BoardOpenTime.objects.get(board__id=boards_ids[0], user=user).time
    board2_time = BoardOpenTime.objects.get(board__id=boards_ids[1], user=user).time

    assert board2_time > board1_time

    client.logout()
    r = client.get(f"/api/boards/{boards_ids[0]}/")
    assert r.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
def test_get_board_details_on_public_board(
    client, public_board
):
    r = client.get(f"/api/boards/{public_board.id}/")
    assert r.status_code == status.HTTP_200_OK
    assert r.data == BoardDetailSerializer(public_board).data

    client.logout()

    r = client.get(f"/api/boards/{public_board.id}/")
    assert r.data == BoardDetailSerializer(public_board).data

    r = client.get(f"/api/boards/jeden/")
    assert r.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_list_latest_opened_by_user_boards(client, user_with_token, multiple_boards):
    user = user_with_token["user"]
    boards_ids = [i.id for i in multiple_boards]

    r = client.get("/api/boards/latest/")
    assert r.status_code == status.HTTP_200_OK

    last_opened_board_times = (
        BoardOpenTime.objects.filter(board__id__in=boards_ids, user=user)
        .order_by("-time")
        .all()
    )
    for i in range(len(r.data) - 1):
        assert last_opened_board_times[i].time > last_opened_board_times[i + 1].time
        assert r.data[i]["id"] == last_opened_board_times[i].board.id


@pytest.mark.django_db
def test_delete_board(client, user_with_token, workspace, prepared_board):
    user = user_with_token["user"]

    workspace_permissions = WorkspacePermission(
        workspace=workspace,
        user=user,
        access_type=WorkspacePermission.AccessTypes.ADMINISTRATOR,
    )
    workspace_permissions.save()

    r = client.post(
        "/api/boards/",
        {
            "workspace": workspace.id,
            "name": prepared_board.name,
            "access_level": Board.AccessLevels.WORKSPACE,
        },
    )
    board_id = r.data["id"]

    workspace_permissions.access_type = WorkspacePermission.AccessTypes.NORMAL
    workspace_permissions.save()
    r = client.delete(f"/api/boards/{board_id}/")
    assert r.status_code == status.HTTP_403_FORBIDDEN

    workspace_permissions.access_type = WorkspacePermission.AccessTypes.ADMINISTRATOR
    workspace_permissions.save()
    r = client.delete(f"/api/boards/{board_id}/")
    assert r.status_code == status.HTTP_204_NO_CONTENT
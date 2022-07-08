import pytest
from app.boards.models import Board
from app.lists.models import List
from app.workspaces.models import WorkspacePermission
from rest_framework import status

from app.boards.serializers import ListSerializer
from model_bakery import baker


@pytest.mark.django_db
def test_create_list(client, workspace, user, board):
    workspace_permission = WorkspacePermission.objects.create(
        workspace=workspace,
        user=user,
        access_type=WorkspacePermission.AccessTypes.OBSERVER
    )
    json = {
        "board": board.id,
        "name": "HelloWorld!?",
        'position': 1
    }

    r = client.post('/api/lists/', json)
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert r.data == {'board': ["You don't have sufficient permissions on particular workspace"]}
    
    workspace_permission.access_type = WorkspacePermission.AccessTypes.NORMAL
    workspace_permission.save()

    r = client.post('/api/lists/', json)
    list = List.objects.get(id=r.data['id'])
    assert r.status_code == status.HTTP_201_CREATED
    assert r.data == ListSerializer(list).data

    client.logout()
    r = client.post('/api/lists/', json)
    assert r.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_modify_list(client, workspace, user, board, list):
    workspace_permission = WorkspacePermission.objects.create(
        workspace=workspace,
        user=user,
        access_type=WorkspacePermission.AccessTypes.OBSERVER
    )
    json = {
        "board": board.id,
        "name": "HelloWorld!?"
    }

    r = client.patch(f'/api/lists/{list.id}/', json)
    assert r.status_code == status.HTTP_403_FORBIDDEN

    workspace_permission.access_type = WorkspacePermission.AccessTypes.NORMAL
    workspace_permission.save()
    r = client.patch(f'/api/lists/{list.id}/', json)
    list = List.objects.get(id=r.data['id'])
    assert r.status_code == status.HTTP_200_OK
    assert r.data == ListSerializer(list).data

    r = client.patch('/api/lists/twojastara/', json)
    assert r.status_code == status.HTTP_404_NOT_FOUND
    
    r = client.patch(f'/api/lists/{list.id}/', {"board": 2} )
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert r.data == {"board": ['Invalid pk "2" - object does not exist.']}

    board2 = baker.make(Board)
    r = client.patch(f'/api/lists/{list.id}/', {"board": board2.id} )
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert r.data == {"board": ["You don't have sufficient permissions on particular workspace"]}

    r = client.patch(f'/api/lists/{list.id}/',{'name': 'None'})
    assert r.status_code == status.HTTP_200_OK

    client.logout()
    r = client.patch(f'/api/lists/{list.id}/', json)
    assert r.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_delete_list(client, workspace, user, list):
    workspace_permission = WorkspacePermission.objects.create(
        workspace=workspace,
        user=user,
        access_type=WorkspacePermission.AccessTypes.OBSERVER
    )
    
    r = client.delete(f'/api/lists/{list.id}/')
    assert r.status_code == status.HTTP_403_FORBIDDEN

    workspace_permission.access_type = WorkspacePermission.AccessTypes.NORMAL
    workspace_permission.save()
    
    r = client.delete(f'/api/lists/{list.id}/')
    assert r.status_code == status.HTTP_204_NO_CONTENT

    client.logout()
    r = client.delete(f'/api/lists/{list.id}/')
    assert r.status_code == status.HTTP_401_UNAUTHORIZED

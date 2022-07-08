import pytest
from app.boards.models import Board
from app.cards.models import Card
from app.workspaces.models import WorkspacePermission
from rest_framework import status

from app.cards.serializers import CardSerializer
from model_bakery import baker

@pytest.mark.django_db
def test_create_card(client, workspace, user, board, list, make_file):
    workspace_permission = WorkspacePermission.objects.create(
        workspace=workspace,
        user=user,
        access_type=WorkspacePermission.AccessTypes.OBSERVER
    )
    form = {
        "board": board.id,
        'list': list.id,
        'position': 1, 
        "name":'Hello',
        'description':'hello',
    }

    r = client.post('/api/cards/', form)
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert r.data == {'board': ["You don't have sufficient permissions on particular workspace"]}
    
    workspace_permission.access_type = WorkspacePermission.AccessTypes.NORMAL
    workspace_permission.save()
    
    r = client.post('/api/cards/', form)
    card = Card.objects.get(id=r.data['id'])
    assert r.status_code == status.HTTP_201_CREATED
    assert r.data == CardSerializer(card).data

    client.logout()
    r = client.post('/api/cards/', form)
    assert r.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_modify_card(client, workspace, user, board, card):
    workspace_permission = WorkspacePermission.objects.create(
        workspace=workspace,
        user=user,
        access_type=WorkspacePermission.AccessTypes.OBSERVER
    )
    json = {
        "board": board.id,
        "name": "HelloWorld!?"
    }

    r = client.patch(f'/api/cards/{card.id}/', json)
    assert r.status_code == status.HTTP_403_FORBIDDEN

    workspace_permission.access_type = WorkspacePermission.AccessTypes.NORMAL
    workspace_permission.save()
    r = client.patch(f'/api/cards/{card.id}/', json)
    card = Card.objects.get(id=r.data['id'])
    assert r.status_code == status.HTTP_200_OK
    assert r.data == CardSerializer(card).data

    r = client.patch('/api/cards/twojastara/', json)
    assert r.status_code == status.HTTP_404_NOT_FOUND
    
    r = client.patch(f'/api/cards/{card.id}/', {"board": 2} )
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert r.data == {"board": ['Invalid pk "2" - object does not exist.']}

    board2 = baker.make(Board)
    r = client.patch(f'/api/cards/{card.id}/', {"board": board2.id} )
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert r.data == {"board": ["You don't have sufficient permissions on particular workspace"]}

    r = client.patch(f'/api/cards/{card.id}/',{'name': 'None'})
    assert r.status_code == status.HTTP_200_OK

    client.logout()
    r = client.patch(f'/api/cards/{card.id}/', json)
    assert r.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_delete_card(client, workspace, user, card):
    workspace_permission = WorkspacePermission.objects.create(
        workspace=workspace,
        user=user,
        access_type=WorkspacePermission.AccessTypes.OBSERVER
    )
    
    r = client.delete(f'/api/cards/{card.id}/')
    assert r.status_code == status.HTTP_403_FORBIDDEN

    workspace_permission.access_type = WorkspacePermission.AccessTypes.NORMAL
    workspace_permission.save()
    
    r = client.delete(f'/api/cards/{card.id}/')
    assert r.status_code == status.HTTP_204_NO_CONTENT

    client.logout()
    r = client.delete(f'/api/cards/{card.id}/')
    assert r.status_code == status.HTTP_401_UNAUTHORIZED

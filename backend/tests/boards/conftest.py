import pytest
from app.boards.models import Board, BoardOpenTime
from app.lists.models import List
from app.workspaces.models import WorkspacePermission
from model_bakery import baker


@pytest.fixture
def prepared_board():
    return baker.prepare(Board)

@pytest.fixture
def public_board(board):
    board.access_level = Board.AccessLevels.PUBLIC
    board.save()
    return board

@pytest.fixture
def multiple_boards(workspace, user):
    WorkspacePermission.objects.create(
        workspace=workspace,
        user=user,
        access_type=WorkspacePermission.AccessTypes.ADMINISTRATOR,
    )

    boards = baker.make(Board, workspace=workspace, _quantity=10)
    for b in boards:
        baker.make(BoardOpenTime, board=b, user=user)
    return boards
import pytest
from app.users.models import CustomUser
from app.workspaces.models import Workspace
from model_bakery import baker
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from app.lists.models import List
from app.cards.models import Card

from app.boards.models import Board, BoardOpenTime

from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO


class CustomAPIClient(APIClient):
    def set_token(self, token: str):
        self.credentials(HTTP_AUTHORIZATION="Token  " + token)


@pytest.fixture
def user():
    return baker.make(CustomUser, email="321@gmail.com")


@pytest.fixture
def user_with_token(user):
    return {"user": user, "token": Token.objects.create(user=user).key}


@pytest.fixture
def user2():
    return baker.make(CustomUser, email="123@gmail.com")


@pytest.fixture
def user2_with_token(user2):
    return {"user": user2, "token": Token.objects.create(user=user2).key}


@pytest.fixture
def workspace():
    return baker.make(Workspace)


@pytest.fixture
def client(user_with_token):
    c = CustomAPIClient()
    c.set_token(user_with_token["token"])
    return c

@pytest.fixture
def board(workspace, user):
    board = baker.make(Board, workspace=workspace)
    baker.make(BoardOpenTime, board=board, user=user)
    return board

@pytest.fixture
def list(board):
    return baker.make(List, board=board)

@pytest.fixture
def card(board):
    return baker.make(Card, board=board)

@pytest.fixture
def make_file():
    def wrapper(file_name, content_type):
        io = BytesIO()
        # This bytes represent required gif headers
        io.write(
            (
                b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
                b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
                b"\x02\x4c\x01\x00\x3b"
            )
        )
        video = InMemoryUploadedFile(io, None, file_name, content_type, 10000, None)
        video.seek(0)
        return video

    return wrapper
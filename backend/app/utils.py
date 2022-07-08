from typing import Optional
from app.workspaces.models import Workspace
from app.lists.models import List
from app.cards.models import Card
from app.boards.models import Board

def extract_workspace_from_obj(obj) -> Optional[Workspace]:
    if isinstance(obj, Board):
        return obj.workspace
    elif isinstance(obj, List) or isinstance(obj, Card):
        return obj.board.workspace
    return None
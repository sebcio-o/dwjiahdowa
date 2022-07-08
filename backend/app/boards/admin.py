from app.boards.models import Board, BoardOpenTime
from django.contrib import admin


admin.site.register([Board, BoardOpenTime])

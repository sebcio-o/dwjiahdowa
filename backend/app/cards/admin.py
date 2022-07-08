from app.cards.models import Card
from django.contrib import admin


class CardAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "last_edited", "created_at")


admin.site.register(Card, CardAdmin)

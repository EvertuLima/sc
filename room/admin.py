from django.contrib import admin  # type: ignore

from room.models import Component, Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "responsible")
    search_fields = ("name", "description", "responsible__username")


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = (
        "inventory_number",
        "description",
        "brand",
        "model",
        "condition",
        "notes",
        "location",
    )
    search_fields = (
        "inventory_number",
        "description",
        "brand",
        "model",
        "condition",
        "location__name",
    )
    list_per_page = 10

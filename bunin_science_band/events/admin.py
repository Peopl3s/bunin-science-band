from django.contrib import admin
from .models import Event, EventImage
from memebers.models import Member
from viewer.models import Viewer


@admin.register(EventImage)
class EventImageAdmin(admin.ModelAdmin):
    """Блок админ-панели для Изображений."""

    list_display = ["image"]


class EventImageInline(admin.TabularInline):
    """Блок админ-панели для Изображений, связанных с Событием."""

    list_display = ["image"]
    model = Event.images.through


class MemberInline(admin.TabularInline):
    """Блок админ-панели для Участников, связанных с Событием."""

    model = Event.members.through


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Блок админ-панели для Событий."""

    exclude = ("members",)
    inlines = [
        EventImageInline,
        MemberInline,
    ]
    list_display = ["title", "slug", "publish", "status", "document"]
    list_filter = ["status", "created", "publish"]
    search_fields = ["title", "body"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "publish"
    ordering = ["status", "publish"]

from django.contrib import admin
from .models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    """Блок админ-панели для Участников."""

    list_display = [
        "name",
        "surname",
        "midname",
        "science_fields",
        "phone",
        "email",
        "socials",
        "rank",
        "description",
        "publish",
        "status",
        "slug",
    ]
    list_filter = ["rank", "status", "created", "publish", "surname", "science_fields"]
    search_fields = ["description", "rank", "surname"]
    prepopulated_fields = {
        "slug": (
            "surname",
            "rank",
        )
    }
    date_hierarchy = "publish"
    ordering = ["status", "publish", "rank"]

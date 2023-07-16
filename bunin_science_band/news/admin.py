from django.contrib import admin
from .models import News, NewsImage
from viewer.models import Viewer


@admin.register(Viewer)
class ViewerAdmin(admin.ModelAdmin):
    """Блок админ-панели для Просмотров."""

    pass


@admin.register(NewsImage)
class NewsImagAdmin(admin.ModelAdmin):
    """Блок админ-панели для Изображений."""

    pass


class NewsImageInline(admin.TabularInline):
    """Блок админ-панели для Изображений, связанных с Новостью."""

    model = News.images.through


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """Блок админ-панели для Новостей."""

    inlines = [
        NewsImageInline,
    ]
    list_display = ["title", "slug", "author", "publish", "status"]
    list_filter = ["status", "created", "publish", "author"]
    search_fields = ["title", "body"]
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ["author"]
    date_hierarchy = "publish"
    ordering = ["status", "publish"]

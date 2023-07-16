from django.contrib.sitemaps import Sitemap
from news.models import News
from events.models import Event
from memebers.models import Member


class NewsSitemap(Sitemap):
    """Карта для записей-новостей."""

    changefreq = "weekly"
    priority = 0.9

    def items(self):
        """Возвращает список всех новостей."""

        return News.objects.all()

    def lastmod(self, obj):
        """Возвращает дату и время публикации записи."""

        return obj.publish


class EventsSitemap(Sitemap):
    """Карта для записей-событий."""

    changefreq = "weekly"
    priority = 0.9

    def items(self):
        """Возвращает список всех событий."""

        return Event.objects.all()

    def lastmod(self, obj):
        """Возвращает дату и время публикации записи."""

        return obj.publish


class MembersSitemap(Sitemap):
    """Карта для записей-участников."""

    changefreq = "weekly"
    priority = 0.9

    def items(self):
        """Возвращает список всех участников."""
        return Member.objects.all()

    def lastmod(self, obj):
        """Возвращает дату и время публикации записи."""
        return obj.publish

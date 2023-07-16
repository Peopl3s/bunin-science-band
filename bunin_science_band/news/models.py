from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from taggit.managers import TaggableManager
from viewer.models import Viewer


class PublishedManager(models.Manager):
    """Менеджер для Новостей."""

    def get_queryset(self):
        """Возвращает список всех опубликованных Новостей."""

        return super().get_queryset().filter(status=News.Status.PUBLISHED)


class News(models.Model):
    """Модель новостей сообщества."""

    class Status(models.TextChoices):
        """Статус записи на сайте."""

        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    viewes = models.ManyToManyField(
        Viewer,
        related_name="views",
        blank=True,
        null=True,
        verbose_name="Просмотры",
    )
    likes = models.ManyToManyField(
        User,
        related_name="news_likes",
        blank=True,
        null=True,
        verbose_name="Лайки",
    )
    title = models.CharField(max_length=250, verbose_name="Заголовок")
    slug = models.SlugField(
        max_length=250, unique_for_date="publish", verbose_name="Слаг"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="news_news",
        verbose_name="Автор",
    )
    body = models.TextField(verbose_name="Содержание")
    publish = models.DateTimeField(
        default=timezone.now(), verbose_name="Дата и время публикации"
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время создания"
    )
    updated = models.DateTimeField(
        auto_now=True, verbose_name="Дата и время обновления"
    )
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name="Статус",
    )

    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.
    tags = TaggableManager()

    class Meta:
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["-publish"]),
        ]
        verbose_name = _("news")
        verbose_name_plural = _("news")

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse(
            "news:news_detail",
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug,
            ],
        )

    def total_views(self) -> int:
        """Возвращает количество просмотров на новосте."""

        return self.viewes.count()

    def number_of_likes(self) -> int:
        """Возвращает количество лайков на записе."""

        return self.likes.count()


class NewsImage(models.Model):
    """Модель изображения, связанного с Новостью."""

    news = models.ManyToManyField(
        News, related_name="images", blank=True, verbose_name="Новость"
    )
    image = models.ImageField(
        upload_to="users/%Y/%m/%d/", blank=True, verbose_name="Изображение"
    )

    def __str__(self) -> str:
        return str(self.image)

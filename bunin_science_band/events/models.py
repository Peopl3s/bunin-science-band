from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from taggit.managers import TaggableManager
from memebers.models import Member
from viewer.models import Viewer


class PublishedManager(models.Manager):
    """Менеджер для Событий."""

    def get_queryset(self):
        """Возвращает список всех опубликованных Событий."""

        return super().get_queryset().filter(status=Event.Status.PUBLISHED)


class Event(models.Model):
    """Модель событий сообщества."""

    class Status(models.TextChoices):
        """Статус записи на сайте."""

        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    viewes = models.ManyToManyField(
        Viewer,
        related_name="viewes",
        blank=True,
        null=True,
        verbose_name="Просмотры",
    )
    title = models.CharField(max_length=250, verbose_name="Заголовок")
    slug = models.SlugField(
        max_length=250, unique_for_date="publish", verbose_name="Slug"
    )
    members = models.ManyToManyField(
        Member,
        related_name="members",
        blank=True,
        null=True,
        verbose_name="Участники",
        help_text="Участники, которые организуют событие",
    )
    likes = models.ManyToManyField(
        User,
        related_name="event_likes",
        blank=True,
        null=True,
        verbose_name="Лайки",
    )
    body = models.TextField(
        verbose_name="Содержимое", help_text="Введите текст о Событии"
    )
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
    document = models.FileField(
        upload_to="events/%Y/%m/%d/", blank=True, verbose_name="Документ"
    )

    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.
    tags = TaggableManager()

    class Meta:
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["-publish"]),
        ]
        verbose_name = _("event")
        verbose_name_plural = _("events")

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse(
            "events:events_detail",
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug,
            ],
        )

    def total_views(self) -> int:
        """Возвращает количество просмотров на записе."""

        return self.viewes.count()

    def number_of_likes(self) -> int:
        """Возвращает количество лайков на записе."""

        return self.likes.count()


class EventImage(models.Model):
    """Модель изображения, связанного с Событием."""

    event = models.ManyToManyField(
        Event,
        related_name="images",
        blank=True,
        verbose_name="Событие",
        help_text="Событие связанное с картинкой",
    )
    image = models.ImageField(
        upload_to="event/%Y/%m/%d/", blank=True, verbose_name="Изображение"
    )

    class Meta:
        verbose_name = _("event_img")
        verbose_name_plural = _("event_imgs")

    def __str__(self) -> str:
        return self.image

from django.db import models
from django.utils.translation import gettext as _
from events.models import Event
from news.models import News


class Comment(models.Model):
    """Модель комментариев для записей."""

    events = models.ForeignKey(
        Event,
        related_name="comments",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="События",
    )
    news = models.ForeignKey(
        News,
        on_delete=models.SET_NULL,
        related_name="comments",
        blank=True,
        null=True,
        verbose_name="Новости",
    )
    name = models.CharField(max_length=80, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    body = models.TextField(verbose_name="Содержимое")
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время создания"
    )
    updated = models.DateTimeField(
        auto_now=True, verbose_name="Дата и время обновления"
    )
    active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        ordering = ["created"]
        indexes = [
            models.Index(fields=["created"]),
        ]

    def __str__(self):
        return f"Комментарий от {self.name}:{self.body}"

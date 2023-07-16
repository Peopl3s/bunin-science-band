from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    """Менеджер для участников."""

    def get_queryset(self):
        """Возвращает всех опубликованных участников."""

        return super().get_queryset().filter(status=Member.Status.PUBLISHED)


class Member(models.Model):
    """Модель учатника сообщества."""

    class Status(models.TextChoices):
        """Статус записи на сайте."""

        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    class Rank(models.TextChoices):
        """Должность/звание участника."""

        PHD = "Доктор наук"
        LOWERPHD = "Кандидат наук"
        POSTGRADUATE = "Аспирант"
        MASTER = "Магистр"
        NONE = "Отсутствует"

    name = models.CharField(_("Имя"), max_length=250)
    surname = models.CharField(_("Фамилия"), max_length=250)
    midname = models.CharField(_("Отчество"), max_length=250)
    science_fields = models.CharField(_("Область научных интересов"), max_length=250)
    rank = models.CharField(
        _("Степень/звание"), choices=Rank.choices, default=Rank.NONE, max_length=250
    )

    phone = models.CharField(_("Телефон"), max_length=250, blank=True)
    email = models.CharField(max_length=250, blank=True, verbose_name="Email")
    socials = models.CharField(
        _("Социальные сети"), max_length=250, blank=True, help_text="Ссылки на соцсети"
    )
    description = models.TextField(_("Описание"))
    image = models.ImageField(_("Изображение"), upload_to="users/%Y/%m/%d/", blank=True)

    slug = models.SlugField(_("Слаг"), max_length=250, unique_for_date="publish")
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
        ordering = ["-surname"]
        indexes = [
            models.Index(fields=["-surname", "-publish", "-status"]),
        ]
        verbose_name = _("member")
        verbose_name_plural = _("members")

    def __str__(self) -> str:
        return f"{self.surname} {self.name} {self.midname}"

    def get_absolute_url(self):
        return reverse(
            "members:members_detail",
            args=[self.publish.year, self.publish.month, self.publish.day, self.slug],
        )

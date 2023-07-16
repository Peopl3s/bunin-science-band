from django.db import models
from django.conf import settings


class Viewer(models.Model):
    """Модель описывает просмотры на записях (новости, эвеныт, участники и т.д.)"""

    ipaddress = models.GenericIPAddressField(
        blank=True, null=True, verbose_name="IP-адрес"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Пользователь",
        help_text="Пользователь, который просомтрел запись",
    )

    def __str__(self):
        return f"{self.id}"

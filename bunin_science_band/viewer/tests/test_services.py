from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from django.utils import timezone


from events.models import Event
from viewer.models import Viewer
from ..services import *

User = get_user_model()


class ViewerServicesTest(TestCase):
    """Тестирует сервисные функции для просмотров."""

    def setUp(self):
        self.event = Event.objects.create(
            title="Тестовый ивент",
            body="Тестовое описание",
            publish=timezone.now(),
            slug="testoviy-ivent",
            status=Event.Status.PUBLISHED,
        )

    def test_add_views(self):
        """Проверяет добавление просмотра."""

        add_view(self.event, "127.0.0.1")
        self.assertEqual(
            self.event.total_views(), 1, "Ошибка добавления просмотра"
        )
        add_view(self.event, "127.0.0.1")
        self.assertEqual(
            self.event.total_views(), 1, "Просмотр не должен быть засчитан"
        )
        add_view(self.event, "127.0.0.2")
        self.assertEqual(self.event.total_views(), 2, "Просмотр не засчитан")

    def test_correct_ip(self):
        """Проверяет корректность получения ip адреса."""

        x_forwarded1 = "127.0.0.1,10.40.0.1,10.40.8.11"
        remote_addr = "127.0.0.1"
        self.assertEqual(
            get_client_ip(x_forwarded1, remote_addr),
            "10.40.8.11",
            "Неправильно определён ip",
        )
        self.assertEqual(
            get_client_ip("", remote_addr),
            "127.0.0.1",
            "Неправильно определён ip",
        )

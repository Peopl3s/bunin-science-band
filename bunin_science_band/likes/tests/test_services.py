from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from http import HTTPStatus
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.core.mail import send_mail
from taggit.models import Tag
import utils.list_helper as list_helper

from events.models import Event
from ..services import add_like

User = get_user_model()


class ServicesTest(TestCase):
    """Тестирует сервисные функции событи."""

    def setUp(self):
        self.user = User.objects.create_user(username="auth", email="test@test.ru")
        self.event1 = Event.objects.create(
            title="Тестовый ивент",
            body="Тестовое описание",
            publish=timezone.now(),
            slug="testoviy-ivent",
            status=Event.Status.PUBLISHED,
        )

    def test_add_like(self):
        """Проверяет добавление и удаление лайков."""
        add_like(self.event1, self.user.id)
        self.assertEqual(self.event1.number_of_likes(), 1, "Ошибка добавления лайка")
        add_like(self.event1, self.user.id)
        self.assertEqual(self.event1.number_of_likes(), 0, "Ошибка удаления лайка")

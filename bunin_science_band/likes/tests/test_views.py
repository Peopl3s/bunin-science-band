from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from http import HTTPStatus
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from events.models import Event
from comments.models import Comment
from memebers.models import Member
from viewer.models import Viewer

User = get_user_model()


class LikesViewsTests(TestCase):
    """Проверка предствлений лайков."""

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username="auth", email="test@test.ru")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        self.event = Event.objects.create(
            title="Тестовый ивент",
            body="Тестовое описание",
            publish=timezone.now(),
            slug="testoviy-ivent",
            status=Event.Status.PUBLISHED,
        )
        self.event.tags.add("django")

    def test_correct_add_like_authorized_client(self):
        """Проверяет корректность добавления лайка авторизованным пользователем."""

        response = self.authorized_client.post(
            reverse("events:events_like", args=[self.event.id])
        )
        self.assertEqual(self.event.number_of_likes(), 1, "Ошибка добавления лайка")
        response = self.authorized_client.post(
            reverse("events:events_like", args=[self.event.id])
        )
        self.assertEqual(self.event.number_of_likes(), 0, "Ошибка удаления лайка")

    def test_correct_add_like_unauthorized_client(self):
        """Проверяет корректность добавления лайка неавторизованным пользователем."""

        response = self.guest_client.post(
            reverse("events:events_like", args=[self.event.id])
        )
        self.assertEqual(self.event.number_of_likes(), 0, "Ошибка добавления лайка")
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

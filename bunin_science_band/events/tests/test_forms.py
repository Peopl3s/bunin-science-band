from http import HTTPStatus
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Event
from comments.models import Comment

User = get_user_model()


class EmailEventFormTests(TestCase):
    """Проверка формы для репоста новости по email"""

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username="auth")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        self.event = Event.objects.create(
            title="Тестовый ивент",
            body="Тестовое описание",
            status=Event.Status.PUBLISHED,
            slug="testoviy-ivent",
        )

        self.event.tags.add("django")

    def test_share_event(self):
        """Проверка репоста новостей по email."""

        form_data = {"name": "Text", "to": "test@mail.ru", "comments": "test"}
        response = self.authorized_client.post(
            reverse(
                "events:events_share",
                args=[
                    self.event.id,
                ],
            ),
            data=form_data,
            follow=True,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_body_null(self):
        """Проверка что тело комментария можно не указывать."""

        form_data = {"name": "Text", "to": "test@mail.ru", "comments": ""}

        response = self.authorized_client.post(
            reverse(
                "events:events_share",
                args=[
                    self.event.id,
                ],
            ),
            data=form_data,
            follow=True,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_reddirect_guest_client(self):
        """ "Проверка редиректа неавторизованного пользователя"""

        form_data = {"name": "Text", "to": "test@mail.ru", "comments": "test"}
        response = self.guest_client.post(
            reverse(
                "events:events_share",
                args=[
                    self.event.id,
                ],
            ),
            data=form_data,
            follow=True,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(
            response, f"/account/login/?next=/events/{self.event.id}/share/"
        )

    def tearDown(self):
        Event.objects.all().delete()


class SearchEventFormTests(TestCase):
    """Проверка формы поиска по новостям."""

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username="auth")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_access_guest_client(self):
        """Проверка возможности поиска неавторизованным пользователем."""

        form_data = {"query": "Test"}
        response = self.guest_client.get(
            reverse("events:events_search"), data=form_data, follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_access_authorized_client(self):
        """Проверка возможности поиска авторизованным пользователем."""

        form_data = {"query": "Test"}
        response = self.authorized_client.get(
            reverse("events:events_search"), data=form_data, follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_null_query(self):
        """Проверка пустого запроса."""

        form_data = {"query": ""}
        response = self.authorized_client.get(
            reverse("events:events_search"), data=form_data, follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def tearDown(self):
        Event.objects.all().delete()


class CommentEventFormTests(TestCase):
    """Проверка формы для комментирования новости."""

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(
            username="auth", email="test@mail.ru"
        )
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        self.event = Event.objects.create(
            title="Тестовый ивент",
            body="Тестовое описание",
            status=Event.Status.PUBLISHED,
            slug="testoviy-ivent",
        )

        self.event.tags.add("django")

    def test_create_comment(self):
        """Проверка создания комментария"""
        comments_count = Comment.objects.count()
        form_data = {"body": "test"}

        response = self.authorized_client.post(
            reverse(
                "events:events_comment",
                args=[
                    self.event.id,
                ],
            ),
            data=form_data,
            follow=True,
        )
        error_name1 = "Данные поста не совпадают"
        self.assertEqual(response.status_code, HTTPStatus.OK)

        c = Comment.objects.filter(body="test")

        self.assertTrue(c.exists(), error_name1)
        error_name2 = "Поcт не добавлен в базу данных"
        self.assertEqual(
            Comment.objects.count(), comments_count + 1, error_name2
        )

    def test_redirect_guest_client(self):
        """ "Проверка редиректа неавторизованного пользователя."""

        form_data = {"body": "test"}
        response = self.guest_client.post(
            reverse(
                "events:events_comment",
                args=[
                    self.event.id,
                ],
            ),
            data=form_data,
            follow=True,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(
            response, f"/account/login/?next=/events/{self.event.id}/comment/"
        )

    def tearDown(self):
        Event.objects.all().delete()

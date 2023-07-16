from django.test import TestCase, Client
from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from taggit.models import Tag

from ..models import News
from comments.models import Comment

User = get_user_model()


class StaticURLTests(TestCase):
    """Проверка статичных страниц."""

    def setUp(self):
        # Создаем неавторизованый клиент
        self.guest_client = Client()

    def test_static_page(self) -> None:
        """Страница доступка по URL."""

        pages: tuple = ("/news/", "/news/search/")
        for page in pages:
            response = self.guest_client.get(page)
            error_name: str = f"Ошибка: нет доступа до страницы {page}"
            self.assertEqual(response.status_code, HTTPStatus.OK, error_name)

    def test_urls_uses_correct_template(self) -> None:
        """URL-адрес использует соответствующий шаблон."""

        templates_url_names: dict = {
            "/news/": "news/news/list.html",
            "/news/search/": "news/news/search.html",
        }
        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.guest_client.get(adress)
                error_name: str = f"Ошибка: {adress} ожидал шаблон {template}"
                self.assertTemplateUsed(response, template, error_name)

    def tearDown(self):
        News.objects.all().delete()


class DynamicURLTests(TestCase):
    """Проверка динамических страниц."""

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username="auth")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        self.news = News.objects.create(
            title="Тестовая новость",
            author=self.user,
            body="Тестовое описание",
            status=News.Status.PUBLISHED,
            slug="testovay-novost",
        )

        self.news.tags.add("django")

        self.comment = Comment.objects.create(
            name=self.user.username,
            email="test@mail.ru",
            body="Тестовое сообщение",
            news=self.news,
            active=True,
        )

    def test_urls_guest_client(self):
        """Доступ неавторизованного пользователя."""

        pages: tuple = (
            f"/news/tag/{self.news.tags.all()[0].slug}/",
            f"{self.news.get_absolute_url()}",
        )
        for page in pages:
            response = self.guest_client.get(page)
            error_name = f"Ошибка: нет доступа до страницы {page}"
            self.assertEqual(response.status_code, HTTPStatus.OK, error_name)

    def test_urls_redirect_guest_client(self):
        """Редирект неавторизованного пользователя"""

        share_redirect_url = f"/account/login/?next=/news/{self.news.id}/share/"

        pages = {f"/news/{self.news.id}/share/": share_redirect_url}
        for page, value in pages.items():
            response = self.guest_client.get(page)
            self.assertRedirects(response, value)

    def test_urls_authorized_client(self):
        """Доступ авторизованного пользователя."""

        get_query = f"/news/{self.news.id}/share/"
        response = self.authorized_client.get(get_query)
        error_name = f"Ошибка: нет доступа до страницы {get_query}"
        self.assertEqual(response.status_code, HTTPStatus.OK, error_name)

        post_query = f"/news/{self.news.id}/comment/"
        response = self.authorized_client.post(post_query)
        error_name = f"Ошибка: нет доступа до страницы {post_query}"
        self.assertEqual(response.status_code, HTTPStatus.OK, error_name)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""

        templates_url_names_get: dict = {
            f"/news/tag/{self.news.tags.all()[0].slug}/": "news/news/list.html",
            f"{self.news.get_absolute_url()}": "news/news/detail.html",
            f"/news/{self.news.id}/share/": "news/news/share.html",
        }

        for adress, template in templates_url_names_get.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                error_name = f"Ошибка: {adress} ожидал шаблон {template}"
                self.assertTemplateUsed(response, template, error_name)

    def tearDown(self):
        News.objects.all().delete()

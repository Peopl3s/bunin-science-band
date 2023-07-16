from django.test import TestCase, Client
from http import HTTPStatus
from django.contrib.auth import get_user_model
from mock import patch
from django.core.exceptions import SuspiciousOperation, PermissionDenied
from django.http import Http404
from ..views import index
from events.models import Event
from django.http import HttpRequest
from django import forms
from django.urls import reverse
from django.db.models.manager import Manager

User = get_user_model()


class StaticURLTests(TestCase):
    """Проверка статичных страниц."""

    def setUp(self):
        # Создаем неавторизованый клиент
        self.guest_client = Client()

    def test_static_page(self) -> None:
        """Страница доступка по URL."""

        pages: tuple = ("/",)
        for page in pages:
            response = self.guest_client.get(page)
            error_name: str = f"Ошибка: нет доступа до страницы {page}"
            self.assertEqual(response.status_code, HTTPStatus.OK, error_name)

    def test_urls_uses_correct_template(self) -> None:
        """URL-адрес использует соответствующий шаблон."""

        templates_url_names: dict = {
            "/": "home/index.html",
        }
        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.guest_client.get(adress)
                error_name: str = f"Ошибка: {adress} ожидал шаблон {template}"
                self.assertTemplateUsed(response, template, error_name)


class ErrorUrlsTests(TestCase):
    """Проверка страниц c ошибками 404 и 500."""

    def setUp(self):
        # Создаем неавторизованый клиент
        self.guest_client = Client()

    def raise_(exception):
        def wrapped(*args, **kwargs):
            raise exception("Test exception")

        return wrapped

    def test_404_page(self) -> None:
        """Проверка 404 страницы."""

        page = "/355445"
        response = self.guest_client.get(page)
        error_name: str = f"Ошибка: нет доступа до страницы {page}"
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND, error_name)

    def test_500_page(self):
        """Проверяет 500 кастомную страницу ошибки."""

        response = self.guest_client.get("/500/")
        self.assertEqual(response.status_code, 500)

    def test_urls_uses_correct_template(self) -> None:
        """URL-адрес использует соответствующий шаблон кастомной 404 страницы."""

        templates_url_names: dict = {
            "/home/232323": "errors/404.html",
        }
        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.guest_client.get(adress)
                error_name: str = f"Ошибка: {adress} ожидал шаблон {template}"
                self.assertTemplateUsed(response, template, error_name)

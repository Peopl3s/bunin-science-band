from django.test import TestCase, Client
from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class StaticURLTests(TestCase):
    """Проверка статичных страниц."""

    def setUp(self):
        # Создаем неавторизованый клиент
        self.guest_client = Client()

    def test_static_page(self) -> None:
        """Страница доступка по URL."""

        pages: tuple = (reverse("contacts:contacts"),)
        for page in pages:
            response = self.guest_client.get(page)
            error_name: str = f"Ошибка: нет доступа до страницы {page}"
            self.assertEqual(response.status_code, HTTPStatus.OK, error_name)

    def test_urls_uses_correct_template(self) -> None:
        """URL-адрес использует соответствующий шаблон."""

        templates_url_names: dict = {reverse("contacts:contacts"): "info/contacts.html"}
        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.guest_client.get(adress)
                error_name: str = f"Ошибка: {adress} ожидал шаблон {template}"
                self.assertTemplateUsed(response, template, error_name)

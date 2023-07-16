from django.test import TestCase, Client
from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class AccountURLTests(TestCase):
    """Проверка статичных страниц."""

    def setUp(self):
        # Создаем неавторизованый клиент
        self.guest_client = Client()
        self.user = User.objects.create_user(username="auth")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_static_page(self) -> None:
        """Страница доступка по URL."""

        pages: tuple = (
            reverse("account:register"),
            reverse("account:login"),
            reverse("account:logout"),
            reverse("account:password_reset"),
            reverse("account:password_reset_complete"),
        )
        for page in pages:
            response = self.authorized_client.get(page)
            error_name: str = f"Ошибка: нет доступа до страницы {page}"
            self.assertEqual(response.status_code, HTTPStatus.OK, error_name)

    def test_urls_uses_correct_template(self) -> None:
        """URL-адрес использует соответствующий шаблон."""

        templates_url_names: dict = {
            reverse("account:register"): "account/account/register.html",
            reverse("account:login"): "account/registration/login.html",
            reverse("account:logout"): "account/registration/logged_out.html",
            reverse(
                "account:password_reset"
            ): "registration/password_reset_form.html",
            reverse(
                "account:password_reset_complete"
            ): "account/registration/password_reset_complete.html",
        }
        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                error_name: str = f"Ошибка: {adress} ожидал шаблон {template}"
                self.assertTemplateUsed(response, template, error_name)

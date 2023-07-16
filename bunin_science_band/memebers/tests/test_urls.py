from django.test import TestCase, Client
from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse
from taggit.models import Tag


from memebers.models import Member

User = get_user_model()


class StaticURLTests(TestCase):
    """Проверка статичных страниц."""

    def setUp(self):
        # Создаем неавторизованый клиент
        self.guest_client = Client()

    def test_static_page(self) -> None:
        """Страница доступка по URL."""

        pages: tuple = ("/members/",)
        for page in pages:
            response = self.guest_client.get(page)
            error_name: str = f"Ошибка: нет доступа до страницы {page}"
            self.assertEqual(response.status_code, HTTPStatus.OK, error_name)

    def test_urls_uses_correct_template(self) -> None:
        """URL-адрес использует соответствующий шаблон."""

        templates_url_names: dict = {
            "/members/": "members/members/list.html",
        }
        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.guest_client.get(adress)
                error_name: str = f"Ошибка: {adress} ожидал шаблон {template}"
                self.assertTemplateUsed(response, template, error_name)


class DynamicURLTests(TestCase):
    """Проверка динамических страниц."""

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username="auth")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.member = Member.objects.create(
            name="test",
            surname="test",
            midname="test",
            science_fields="test",
            rank=Member.Rank.PHD,
            phone="test",
            email="test",
            socials="test",
            description="test",
            slug="test-doktor-nauk",
            status=Member.Status.PUBLISHED,
        )
        self.member.tags.add("django")

    def test_urls_guest_client(self):
        """Доступ неавторизованного пользователя."""
        pages: tuple = (
            f"/members/tag/{self.member.tags.all()[0].slug}/",
            reverse(
                "members:members_detail",
                args=[*self.member.get_absolute_url().split("/")[2:-1]],
            ),
        )
        for page in pages:
            response = self.guest_client.get(page)
            error_name = f"Ошибка: нет доступа до страницы {page}"
            self.assertEqual(response.status_code, HTTPStatus.OK, error_name)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""

        templates_url_names_get: dict = {
            f"/members/tag/{self.member.tags.all()[0].slug}/": "members/members/list.html",
            f"{self.member.get_absolute_url()}": "members/members/detail.html",
        }

        for adress, template in templates_url_names_get.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                error_name = f"Ошибка: {adress} ожидал шаблон {template}"
                self.assertTemplateUsed(response, template, error_name)

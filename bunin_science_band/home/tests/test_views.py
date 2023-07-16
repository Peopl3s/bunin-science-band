from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from http import HTTPStatus

User = get_user_model()


class HomeViewsTests(TestCase):
    """Проверка предствлений событий."""

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username="auth", email="test@test.ru")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_views_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""

        templates_url_names = {reverse("home:index"): "home/index.html"}
        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                error_name = f"Ошибка: {adress} ожидал шаблон {template}"
                self.assertTemplateUsed(response, template, error_name)

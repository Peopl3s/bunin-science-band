from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from http import HTTPStatus
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.urls import reverse

User = get_user_model()


class AccountViewsTests(TestCase):
    """Проверка предствлений для роботы с аккаунтами."""

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username="auth", email="test@test.ru")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        self.credentials = {"username": "testuser", "password": "secret13231637!H"}
        User.objects.create_user(**self.credentials)

        self.data = {
            "username": "test",
            "email": "test@hotmail.com",
            "password": "tesFDJHJt12345",
            "password2": "tesFDJHJt12345",
        }

    def test_signup_returns_200(self):
        """Проверка корректной обработки входа."""

        response = self.client.get(reverse("account:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/registration/login.html")

    def test_login(self):
        """Проверка входа."""

        response = self.guest_client.post("/account/login/", self.credentials, follow=True)
        self.assertTrue(response.context["user"].is_authenticated)

    def test_new_user_is_registered(self):
        """Проверка регистрации."""

        nb_old_users = User.objects.count()
        self.client.post(reverse("account:register"), self.data)
        nb_new_users = User.objects.count()
        self.assertEqual(nb_new_users, nb_old_users + 1)

    def test_redirect_if_user_is_authenticated(self):
        """Проверка корректного редиректа после входа."""

        login = self.client.login(email="user1@gmail.com", password="1234")
        response = self.guest_client.post(reverse("account:login"), self.credentials)
        self.assertRedirects(response, reverse("home:index"))

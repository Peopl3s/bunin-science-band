from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from http import HTTPStatus
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.core.mail import send_mail
from taggit.models import Tag
import utils.list_helper as list_helper

from ..models import News
from comments.models import Comment
from memebers.models import Member
from viewer.models import Viewer
from ..tasks import share_by_email
from ..services import *

User = get_user_model()


class EmailTest(TestCase):
    def test_send_email(self):
        """Проверяет отправку почты."""
        sent: bool = share_by_email(
            "test", "test", "test_url", "test", "from@example.com", "to@example.com"
        )
        self.assertEqual(sent, True)


class ServicesTest(TestCase):
    """Тестирует сервисные функции новостей."""

    def setUp(self):
        self.user = User.objects.create_user(username="auth", email="user@user.ru")
        self.news1 = News.objects.create(
            title="Тестовая новость",
            author=self.user,
            body="Тестовое описание",
            status=News.Status.PUBLISHED,
            slug="testovay-novost",
        )
        self.news1.tags.add("django")

        self.news2 = News.objects.create(
            title="Тестовая новость2",
            author=self.user,
            body="Тестовое описание2",
            status=News.Status.PUBLISHED,
            slug="testovay-novost2",
        )
        self.news2.tags.add("django")

    def test_all_published_news(self):
        """Проверяет общее количество опубликованных новостей."""

        self.assertEqual(get_all_published_news().count(), 2)

    def test_get_similar_news(self):
        """Проверяет количество список похожих (по количеству общих тегов) Новостей."""

        ids = list_helper.get_resource_tags_ids(self.news1)
        self.assertEqual(len(get_similar_news(ids, self.news1.id, 1)), 1)

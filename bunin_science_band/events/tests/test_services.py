from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from http import HTTPStatus
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.core.mail import send_mail
from taggit.models import Tag
import utils.list_helper as list_helper

from ..models import Event
from comments.models import Comment
from memebers.models import Member
from viewer.models import Viewer
from ..tasks import share_by_email
from ..services import *

User = get_user_model()


class EmailTest(TestCase):
    def test_send_email(self):
        """Проверяет отправку почты."""
        sent: bool = share_by_email("test", "test", "test_url", "test", "from@example.com", "to@example.com")
        self.assertEqual(sent, True)


class ServicesTest(TestCase):
    """Тестирует сервисные функции событи."""

    def setUp(self):
        self.event1 = Event.objects.create(
            title="Тестовый ивент",
            body="Тестовое описание",
            publish=timezone.now(),
            slug="testoviy-ivent",
            status=Event.Status.PUBLISHED,
        )
        self.event1.tags.add("django")

        self.event2 = Event.objects.create(
            title="Тестовый ивент2",
            body="Тестовое описание2",
            publish=timezone.now(),
            slug="testoviy-ivent2",
            status=Event.Status.PUBLISHED,
        )
        self.event2.tags.add("django")

    def test_all_published_events(self):
        """Проверяет общее количество опубликованных новостей."""

        self.assertEqual(get_all_published_events().count(), 2)

    def test_get_similar_events(self):
        """Проверяет количество список похожих (по количеству общих тегов) Событий."""

        ids = list_helper.get_resource_tags_ids(self.event1)
        self.assertEqual(len(get_similar_events(ids, self.event1.id, 1)), 1)

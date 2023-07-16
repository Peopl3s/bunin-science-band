from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from http import HTTPStatus
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.core.mail import send_mail
from taggit.models import Tag
import utils.list_helper as list_helper

from memebers.models import Member
from ..services import *

User = get_user_model()


class ServicesTest(TestCase):
    """Тестирует сервисные функции событи."""

    def setUp(self):
        self.member1 = Member.objects.create(
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
        self.member1.tags.add("django")

        self.member2 = Member.objects.create(
            name="test2",
            surname="test2",
            midname="test2",
            science_fields="test2",
            rank=Member.Rank.PHD,
            phone="test2",
            email="test2",
            socials="test2",
            description="test2",
            slug="test-doktor-nauk2",
            status=Member.Status.PUBLISHED,
        )
        self.member2.tags.add("django")

    def test_all_published_members(self):
        """Проверяет общее количество участников."""

        self.assertEqual(get_all_published_members().count(), 2)

    def test_get_similar_members(self):
        """Проверяет количество список похожих (по количеству общих тегов) Участников."""

        ids = list_helper.get_resource_tags_ids(self.member1)
        self.assertEqual(len(get_similar_members(ids, self.member1.id, 1)), 1)

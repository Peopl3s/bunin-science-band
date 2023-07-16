from http import HTTPStatus
from django.test import Client, TestCase
from django.contrib.auth import get_user_model

from ..models import Event, EventImage
from comments.models import Comment
from memebers.models import Member
from viewer.models import Viewer

User = get_user_model()


class EventModelTest(TestCase):
    """Проверка модели событий."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="auth", email="test@mail.ru"
        )
        self.event = Event.objects.create(
            title="Тестовый ивент",
            body="Тестовое описание",
            status=Event.Status.PUBLISHED,
            slug="testoviy-ivent",
        )
        self.event.tags.add("django")
        self.image = EventImage.objects.create(image="test.png")
        self.image.event.set([self.event])

    def test_title_label(self):
        """Проверка заполнения verbose_name События."""

        field_verboses = {
            "viewes": "Просмотры",
            "title": "Заголовок",
            "slug": "Slug",
            "members": "Участники",
            "likes": "Лайки",
            "body": "Содержимое",
            "publish": "Дата и время публикации",
            "created": "Дата и время создания",
            "updated": "Дата и время обновления",
            "status": "Статус",
            "document": "Документ",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                error_name = f"Поле {field} ожидало значение {expected_value}"
                self.assertEqual(
                    self.event._meta.get_field(field).verbose_name,
                    expected_value,
                    error_name,
                )

    def test_models_have_correct_object_names(self):
        """Проверка __str__ Event."""

        error_name = f"Заголовок не совпадает"
        self.assertEqual(self.event.__str__(), self.event.title, error_name)

    def test_title_help_text(self):
        """Проверка заполнения help_text."""

        field_help_texts = {
            "members": "Участники, которые организуют событие",
            "body": "Введите текст о Событии",
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                error_name = f"Поле {field} ожидало значение {expected_value}"
                self.assertEqual(
                    self.event._meta.get_field(field).help_text,
                    expected_value,
                    error_name,
                )

    def test_event_has_image(self):
        """Проверяет наличие изображений у новости."""

        image2 = EventImage.objects.create(image="test2.png")
        image2.event.set([self.event])

        self.assertEqual(self.image.event.count(), 1)
        self.assertEqual(image2.event.count(), 1)

    def test_event_has_member(self):
        """Проверяет наличие участников у новости."""

        member1 = Member.objects.create(
            name="test",
            surname="test",
            midname="test",
            science_fields="test",
            rank=Member.Rank.PHD,
            phone="test",
            email="test",
            socials="test",
            description="test",
            slug="test",
        )

        member2 = Member.objects.create(
            name="test2",
            surname="test2",
            midname="test2",
            science_fields="test2",
            rank=Member.Rank.PHD,
            phone="test2",
            email="test2",
            socials="test2",
            description="test2",
            slug="test2",
        )

        self.event.members.set([member1, member2])
        self.assertEqual(self.event.members.count(), 2)

    def test_event_has_views(self):
        """Проверяет наличие просмотров у новости."""

        view = Viewer.objects.create(ipaddress="127.0.0.1", user=self.user)
        view2 = Viewer.objects.create(ipaddress="127.0.0.2", user=self.user)
        self.event.viewes.set([view, view2])
        self.assertEqual(self.event.viewes.count(), 2)

    def test_event_has_likes(self):
        """Проверяет наличие лайков у новости."""

        self.event.likes.set([self.user, self.user])
        self.assertEqual(self.event.likes.count(), 1)

    def tearDown(self):
        Event.objects.all().delete()


class EventImageModelTest(TestCase):
    """Проверка модели изображения событий."""

    def setUp(self):
        self.image = EventImage.objects.create(image="test.png")

    def test_title_label(self):
        """Проверка заполнения verbose_name EventImage."""

        field_verboses = {"event": "Событие", "image": "Изображение"}
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                error_name = f"Поле {field} ожидало значение {expected_value}"
                self.assertEqual(
                    self.image._meta.get_field(field).verbose_name,
                    expected_value,
                    error_name,
                )

    def test_models_have_correct_object_names(self):
        """Проверка __str__ EventImage."""

        error_name = f"Заголовок не совпадает"
        self.assertEqual(self.image.__str__(), self.image.image, error_name)

    def test_title_help_text(self):
        """Проверка заполнения help_text."""

        field_help_texts = {"event": "Событие связанное с картинкой"}
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                error_name = f"Поле {field} ожидало значение {expected_value}"
                self.assertEqual(
                    self.image._meta.get_field(field).help_text,
                    expected_value,
                    error_name,
                )

    def tearDown(self):
        Event.objects.all().delete()

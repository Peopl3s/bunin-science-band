from http import HTTPStatus
from django.test import Client, TestCase
from django.contrib.auth import get_user_model

from events.models import Event, EventImage
from comments.models import Comment
from memebers.models import Member
from viewer.models import Viewer

User = get_user_model()


class CommentModelTest(TestCase):
    """Проверка модели Комментариев."""

    def setUp(self):
        self.user = User.objects.create_user(username="auth", email="test@mail.ru")
        self.event = Event.objects.create(
            title="Тестовый ивент",
            body="Тестовое описание",
            status=Event.Status.PUBLISHED,
            slug="testoviy-ivent",
        )
        self.event.tags.add("django")
        self.comment = Comment.objects.create(
            name="test", email="test@test.ru", active=True, events=self.event
        )

    def test_title_label(self):
        """Проверка заполнения verbose_name Комментария."""

        field_verboses = {
            "events": "События",
            "news": "Новости",
            "name": "Имя",
            "email": "Email",
            "body": "Содержимое",
            "created": "Дата и время создания",
            "updated": "Дата и время обновления",
            "active": "Активен",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                error_name = f"Поле {field} ожидало значение {expected_value}"
                self.assertEqual(
                    self.comment._meta.get_field(field).verbose_name,
                    expected_value,
                    error_name,
                )

    def test_models_have_correct_object_names(self):
        """Проверка __str__ Комментарий."""

        error_name = f"Заголовок не совпадает"
        self.assertEqual(
            self.comment.__str__(),
            f"Комментарий от {self.comment.name}:{self.comment.body}",
            error_name,
        )

from http import HTTPStatus
from django.test import Client, TestCase
from django.contrib.auth import get_user_model

from events.models import Event
from memebers.models import Member

User = get_user_model()


class MemberModelTest(TestCase):
    """Проверка модели событий."""

    def setUp(self):
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
            slug="test",
        )

    def test_title_label(self):
        """Проверка заполнения verbose_name Участника."""

        field_verboses = {
            "name": "Имя",
            "surname": "Фамилия",
            "midname": "Отчество",
            "science_fields": "Область научных интересов",
            "rank": "Степень/звание",
            "phone": "Телефон",
            "email": "Email",
            "socials": "Социальные сети",
            "description": "Описание",
            "image": "Изображение",
            "slug": "Слаг",
            "publish": "Дата и время публикации",
            "created": "Дата и время создания",
            "updated": "Дата и время обновления",
            "status": "Статус",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                error_name = f"Поле {field} ожидало значение {expected_value}"
                self.assertEqual(
                    self.member._meta.get_field(field).verbose_name,
                    expected_value,
                    error_name,
                )

    def test_models_have_correct_object_names(self):
        """Проверка __str__ Member."""

        error_name = f"Заголовок не совпадает"
        self.assertEqual(
            self.member.__str__(),
            f"{self.member.surname} {self.member.name} {self.member.midname}",
            error_name,
        )

    def test_title_help_text(self):
        """Проверка заполнения help_text."""

        field_help_texts = {"socials": "Ссылки на соцсети"}
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                error_name = f"Поле {field} ожидало значение {expected_value}"
                self.assertEqual(
                    self.member._meta.get_field(field).help_text,
                    expected_value,
                    error_name,
                )

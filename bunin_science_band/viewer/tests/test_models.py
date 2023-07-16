from http import HTTPStatus
from django.test import Client, TestCase
from django.contrib.auth import get_user_model

from viewer.models import Viewer

User = get_user_model()


class ViewerModelTest(TestCase):
    """Проверка модели Просмотров."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="auth", email="test@mail.ru"
        )
        self.viewer = Viewer.objects.create(
            ipaddress="127.0.0.1", user=self.user
        )

    def test_title_label(self):
        """Проверка заполнения verbose_name События."""

        field_verboses = {"ipaddress": "IP-адрес", "user": "Пользователь"}
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                error_name = f"Поле {field} ожидало значение {expected_value}"
                self.assertEqual(
                    self.viewer._meta.get_field(field).verbose_name,
                    expected_value,
                    error_name,
                )

    def test_models_have_correct_object_names(self):
        """Проверка __str__ Viewer."""

        error_name = f"Заголовок не совпадает"
        self.assertEqual(self.viewer.__str__(), str(self.viewer.id), error_name)

    def test_title_help_text(self):
        """Проверка заполнения help_text."""

        field_help_texts = {"user": "Пользователь, который просомтрел запись"}
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                error_name = f"Поле {field} ожидало значение {expected_value}"
                self.assertEqual(
                    self.viewer._meta.get_field(field).help_text,
                    expected_value,
                    error_name,
                )

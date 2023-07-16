from http import HTTPStatus
from django.test import Client, TestCase
from django.contrib.auth import get_user_model

from ..models import News, NewsImage
from comments.models import Comment
from memebers.models import Member
from viewer.models import Viewer

User = get_user_model()


class NewsModelTest(TestCase):
    """Проверка модели новостей."""

    def setUp(self):
        self.user = User.objects.create_user(username="auth", email="test@mail.ru")
        self.news = News.objects.create(
            title="Тестовая новость",
            author=self.user,
            body="Тестовое описание",
            status=News.Status.PUBLISHED,
            slug="testovay-novost",
        )

        self.news.tags.add("django")
        self.image = NewsImage.objects.create(image="test.png")
        self.image.news.set([self.news])

    def test_title_label(self):
        """Проверка заполнения verbose_name Новости."""

        field_verboses = {
            "viewes": "Просмотры",
            "title": "Заголовок",
            "slug": "Слаг",
            "likes": "Лайки",
            "body": "Содержание",
            "publish": "Дата и время публикации",
            "created": "Дата и время создания",
            "updated": "Дата и время обновления",
            "status": "Статус",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                error_name = f"Поле {field} ожидало значение {expected_value}"
                self.assertEqual(
                    self.news._meta.get_field(field).verbose_name,
                    expected_value,
                    error_name,
                )

    def test_models_have_correct_object_names(self):
        """Проверка __str__ News."""

        error_name = f"Заголовок не совпадает"
        self.assertEqual(self.news.__str__(), self.news.title, error_name)

    def test_news_has_image(self):
        """Проверяет наличие изображений у новости."""

        image2 = NewsImage.objects.create(image="test2.png")
        image2.news.set([self.news])

        self.assertEqual(self.image.news.count(), 1)
        self.assertEqual(image2.news.count(), 1)

    def test_news_has_views(self):
        """Проверяет наличие просмотров у новости."""

        view = Viewer.objects.create(ipaddress="127.0.0.1", user=self.user)
        view2 = Viewer.objects.create(ipaddress="127.0.0.2", user=self.user)
        self.news.viewes.set([view, view2])
        self.assertEqual(self.news.viewes.count(), 2)

    def test_news_has_likes(self):
        """Проверяет наличие лайков у новости."""

        self.news.likes.set([self.user, self.user])
        self.assertEqual(self.news.likes.count(), 1)

    def tearDown(self):
        News.objects.all().delete()


class EventImageModelTest(TestCase):
    """Проверка модели изображения событий."""

    def setUp(self):
        self.image = NewsImage.objects.create(image="test.png")

    def test_title_label(self):
        """Проверка заполнения verbose_name NewsImage."""

        field_verboses = {"news": "Новость", "image": "Изображение"}
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

    def tearDown(self):
        News.objects.all().delete()

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from http import HTTPStatus
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from ..models import News
from comments.models import Comment
from memebers.models import Member
from viewer.models import Viewer
from ..feeds import LatestPostsFeed

User = get_user_model()

NEWS_COUNT = 5
PAGINATE_COUNT = 3


# class PaginatorViewsTest(TestCase):
#     """Проверка пагинации событий."""

#     def setUp(self):
#         self.guest_client = Client()
#         self.user = User.objects.create_user(username="auth")
#         self.authorized_client = Client()
#         self.authorized_client.force_login(self.user)
#         bilk_news: list = []
#         for i in range(NEWS_COUNT):
#             bilk_news.append(
#                 News(
#                     title=f"Тестовая новость{i}",
#                     author=self.user,
#                     body=f"Тестовое описание{i}",
#                     status=News.Status.PUBLISHED,
#                     slug=f"testovay-novost{i}",
#                 )
#             )
#         News.objects.bulk_create(bilk_news)

#     def test_correct_page_context_guest_client(self):
#         """Проверка количества событий на первой и второй страницах."""

#         pages: tuple = (reverse("news:news_list"),)
#         for page in pages:
#             response1 = self.guest_client.get(page)
#             response2 = self.guest_client.get(page + "?page=2")
#             count_posts1 = len(response1.context["news"])
#             count_posts2 = len(response2.context["news"])

#             error_name1 = (
#                 f"Ошибка: {count_posts1} новостей," f" должно быть{PAGINATE_COUNT}"
#             )
#             error_name2 = (
#                 f"Ошибка: {count_posts2} новостей,"
#                 f"должно {NEWS_COUNT - PAGINATE_COUNT}"
#             )
#             self.assertEqual(count_posts1, PAGINATE_COUNT, error_name1)
#             self.assertEqual(count_posts2, NEWS_COUNT - PAGINATE_COUNT, error_name2)

#     def test_correct_page_context_authorized_client(self):
#         """Проверка количества событий на первой и второй
#         страницах авторизованного пользователя."""

#         pages: tuple = (reverse("news:news_list"),)
#         for page in pages:
#             response1 = self.authorized_client.get(page)
#             response2 = self.authorized_client.get(page + "?page=2")
#             count_posts1 = len(response1.context["news"])
#             count_posts2 = len(response2.context["news"])

#             error_name1 = (
#                 f"Ошибка: {count_posts1} новостей," f" должно быть{PAGINATE_COUNT}"
#             )
#             error_name2 = (
#                 f"Ошибка: {count_posts2} новостей,"
#                 f"должно {NEWS_COUNT - PAGINATE_COUNT}"
#             )
#             self.assertEqual(count_posts1, PAGINATE_COUNT, error_name1)
#             self.assertEqual(count_posts2, NEWS_COUNT - PAGINATE_COUNT, error_name2)

#     def tearDown(self):
#         News.objects.all().delete()


class NewsViewsTests(TestCase):
    """Проверка предствлений новости."""

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username="auth", email="test@test.ru")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        self.news = News.objects.create(
            title="Тестовая новость",
            author=self.user,
            body="Тестовое описание",
            status=News.Status.PUBLISHED,
            slug="testovay-novost",
        )
        self.news.tags.add("django")
        self.comment = Comment.objects.create(
            name=self.user.username,
            email="test@mail.ru",
            body="Тестовое сообщение",
            news=self.news,
            active=True,
        )

    def test_views_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""

        templates_url_names = {
            reverse("news:news_list"): "news/news/list.html",
            reverse(
                "news:news_list_by_tag",
                kwargs={"tag_slug": f"{self.news.tags.all()[0].slug}"},
            ): "news/news/list.html",
            reverse(
                "news:news_detail",
                args=[*self.news.get_absolute_url().split("/")[2:-1]],
            ): "news/news/detail.html",
            reverse("news:news_share", args=[self.news.id]): "news/news/share.html",
            reverse("news:news_search"): "news/news/search.html",
        }
        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                error_name = f"Ошибка: {adress} ожидал шаблон {template}"
                self.assertTemplateUsed(response, template, error_name)

    # def test_news_added_correctly(self):
    #     """Новость при создании добавлена корректно."""

    #     one_more_news = News.objects.create(
    #         title="Тестовая новость2",
    #         author=self.user,
    #         body="Тестовое описание2",
    #         status=News.Status.PUBLISHED,
    #         slug="testovay-novost2",
    #     )

    #     one_more_news.tags.add("test")

    #     response_index = self.authorized_client.get(reverse("news:news_list"))

    #     response_share = self.authorized_client.get(
    #         reverse("news:news_share", args=[one_more_news.id])
    #     )

    #     response_detail = self.authorized_client.get(
    #         reverse(
    #             "news:news_detail",
    #             args=[*one_more_news.get_absolute_url().split("/")[2:-1]],
    #         )
    #     )

    #     response_tags = self.authorized_client.get(
    #         reverse(
    #             "news:news_list_by_tag",
    #             kwargs={"tag_slug": f"{one_more_news.tags.all()[0].slug}"},
    #         )
    #     )

    #     response_search = self.authorized_client.get(
    #         reverse("news:news_search"), data={"query": "новость2"}
    #     )

    #     index = response_index.context["news"]
    #     tags = response_tags.context["news"]
    #     share = response_share.context["news"]
    #     detail = response_detail.context["news"]
    #     seacrh = response_search.context["results"]

    #     self.assertIn(one_more_news, index, "новости нет на главной")
    #     self.assertIn(one_more_news, tags, "новости нет в списке по тегам")
    #     self.assertEqual(one_more_news, share, "новость не доступна для репоста")
    #     self.assertEqual(one_more_news, detail, "новости не доступна для просмотра")
    #     self.assertIn(one_more_news, seacrh, "новости не отображается в поиске")

    def test_news_detail_page_show_correct_context(self):
        """Шаблон news_detail сформирован с правильным контекстом."""

        response = self.authorized_client.get(
            reverse(
                "news:news_detail",
                args=[*self.news.get_absolute_url().split("/")[2:-1]],
            )
        )
        post_text_0 = {
            response.context["news"].title: "Тестовая новость",
            response.context["news"].body: "Тестовое описание",
        }
        for value, expected in post_text_0.items():
            self.assertEqual(post_text_0[value], expected)

    def test_news_add_comment_authorized_client(self):
        """Проверка отправки комментария авторизованным пользователем."""

        response = self.authorized_client.post(
            reverse("news:news_comment", args=[self.news.id]), {"body": "test"}
        )
        comments_count = self.news.comments.count()
        self.assertEqual(
            response.status_code, HTTPStatus.OK, "Пользователь не авторизован"
        )
        self.assertEqual(comments_count, 2, "Комментарий не добавлен")

    def test_news_add_comment_guest_client(self):
        """Проверка отправки комментария неавторизованным пользователем."""

        response = self.guest_client.post(
            reverse("news:news_comment", args=[self.news.id]), {"body": "test"}
        )
        comments_count = self.news.comments.count()
        self.assertEqual(
            response.status_code, HTTPStatus.FOUND, "Пользователь не авторизован"
        )
        self.assertEqual(comments_count, 1, "Комментарий не добавлен")

    def test_news_feed(self):
        feed = LatestPostsFeed(1, 10)
        title = feed.item_title(self.news)
        description = feed.item_description(self.news)
        items = feed.items()
        self.assertEqual(title, "Тестовая новость")
        self.assertEqual(description, "<p>Тестовое описание</p>")
        self.assertEqual(len(items), 1)

    def tearDown(self):
        News.objects.all().delete()

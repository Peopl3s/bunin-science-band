from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from http import HTTPStatus
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from ..models import Event
from comments.models import Comment
from memebers.models import Member
from viewer.models import Viewer

User = get_user_model()

EVENTS_COUNT = 5
PAGINATE_COUNT = 3


# class PaginatorViewsTest(TestCase):
#     """Проверка пагинации событий."""

#     def setUp(self):
#         self.guest_client = Client()
#         self.user = User.objects.create_user(username="auth")
#         self.authorized_client = Client()
#         self.authorized_client.force_login(self.user)
#         bilk_events: list = []
#         for i in range(EVENTS_COUNT):
#             bilk_events.append(
#                 Event(
#                     title=f"Тестовый ивент{i}",
#                     body="Тестовое описание",
#                     status=Event.Status.PUBLISHED,
#                     slug=f"testoviy-ivent-{i}",
#                 )
#             )
#         Event.objects.bulk_create(bilk_events)

#     def test_correct_page_context_guest_client(self):
#         """Проверка количества событий на первой и второй страницах."""

#         pages: tuple = (reverse("events:events_list"),)
#         for page in pages:
#             response1 = self.guest_client.get(page)
#             response2 = self.guest_client.get(page + "?page=2")
#             count_posts1 = len(response1.context["events"])
#             count_posts2 = len(response2.context["events"])

#             error_name1 = (
#                 f"Ошибка: {count_posts1} постов," f" должно быть{PAGINATE_COUNT}"
#             )
#             error_name2 = (
#                 f"Ошибка: {count_posts2} постов,"
#                 f"должно {EVENTS_COUNT - PAGINATE_COUNT}"
#             )
#             self.assertEqual(count_posts1, PAGINATE_COUNT, error_name1)
#             self.assertEqual(count_posts2, EVENTS_COUNT - PAGINATE_COUNT, error_name2)

#     def test_correct_page_context_authorized_client(self):
#         """Проверка количества событий на первой и второй
#         страницах авторизованного пользователя."""

#         pages: tuple = (reverse("events:events_list"),)
#         for page in pages:
#             response1 = self.authorized_client.get(page)
#             response2 = self.authorized_client.get(page + "?page=2")
#             count_posts1 = len(response1.context["events"])
#             count_posts2 = len(response2.context["events"])

#             error_name1 = (
#                 f"Ошибка: {count_posts1} постов," f" должно быть{PAGINATE_COUNT}"
#             )
#             error_name2 = (
#                 f"Ошибка: {count_posts2} постов,"
#                 f"должно {EVENTS_COUNT - PAGINATE_COUNT}"
#             )
#             self.assertEqual(count_posts1, PAGINATE_COUNT, error_name1)
#             self.assertEqual(count_posts2, EVENTS_COUNT - PAGINATE_COUNT, error_name2)

#     def tearDown(self):
#         Event.objects.all().delete()


class EventViewsTests(TestCase):
    """Проверка предствлений событий."""

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username="auth", email="test@test.ru")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        self.event = Event.objects.create(
            title="Тестовый ивент",
            body="Тестовое описание",
            publish=timezone.now(),
            slug="testoviy-ivent",
            status=Event.Status.PUBLISHED,
        )
        self.event.tags.add("django")
        self.comment = Comment.objects.create(
            name=self.user.username,
            email="test@mail.ru",
            body="Тестовое сообщение",
            events=self.event,
            active=True,
        )

    def test_views_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""

        templates_url_names = {
            reverse("events:events_list"): "events/events/list.html",
            reverse(
                "events:events_list_by_tag",
                kwargs={"tag_slug": f"{self.event.tags.all()[0].slug}"},
            ): "events/events/list.html",
            reverse(
                "events:events_detail",
                args=[*self.event.get_absolute_url().split("/")[2:-1]],
            ): "events/events/detail.html",
            reverse("events:events_share", args=[self.event.id]): "events/events/share.html",
            reverse("events:events_search"): "events/events/search.html",
        }
        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                error_name = f"Ошибка: {adress} ожидал шаблон {template}"
                self.assertTemplateUsed(response, template, error_name)

    # def test_event_added_correctly(self):
    #     """Новость при создании добавлена корректно."""

    #     one_more_event = Event.objects.create(
    #         title="Ещё тестовый ивент",
    #         body="Ещё тестовое описание",
    #         publish=timezone.now(),
    #         slug="eshe-testoviy-ivent",
    #         status=Event.Status.PUBLISHED,
    #     )
    #     member1 = Member.objects.create(
    #         name="test",
    #         surname="test",
    #         midname="test",
    #         science_fields="test",
    #         rank=Member.Rank.PHD,
    #         phone="test",
    #         email="test",
    #         socials="test",
    #         description="test",
    #         slug="test",
    #     )
    #     one_more_event.tags.add("test")

    #     response_index = self.authorized_client.get(reverse("events:events_list"))

    #     response_share = self.authorized_client.get(
    #         reverse("events:events_share", args=[one_more_event.id])
    #     )

    #     response_detail = self.authorized_client.get(
    #         reverse(
    #             "events:events_detail",
    #             args=[*one_more_event.get_absolute_url().split("/")[2:-1]],
    #         )
    #     )

    #     response_tags = self.authorized_client.get(
    #         reverse(
    #             "events:events_list_by_tag",
    #             kwargs={"tag_slug": f"{one_more_event.tags.all()[0].slug}"},
    #         )
    #     )

    #     response_search = self.authorized_client.get(
    #         reverse("events:events_search"), data={"query": "Ещё"}
    #     )

    #     index = response_index.context["events"]
    #     tags = response_tags.context["events"]
    #     share = response_share.context["events"]
    #     detail = response_detail.context["events"]
    #     seacrh = response_search.context["results"]

    #     self.assertIn(one_more_event, index, "новости нет на главной")
    #     self.assertIn(one_more_event, tags, "новости нет в списке по тегам")
    #     self.assertEqual(one_more_event, share, "новость не доступна для репоста")
    #     self.assertEqual(one_more_event, detail, "новости не доступна для просмотра")
    #     self.assertIn(one_more_event, seacrh, "новости не отображается в поиске")

    def test_event_detail_page_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""

        response = self.authorized_client.get(
            reverse(
                "events:events_detail",
                args=[*self.event.get_absolute_url().split("/")[2:-1]],
            )
        )
        post_text_0 = {
            response.context["events"].title: "Тестовый ивент",
            response.context["events"].body: "Тестовое сообщение",
        }
        for value, expected in post_text_0.items():
            self.assertEqual(post_text_0[value], expected)

    def test_event_add_comment_authorized_client(self):
        """Проверка отправки комментария авторизованным пользователем."""

        response = self.authorized_client.post(reverse("events:events_comment", args=[self.event.id]), {"body": "test"})
        comments_count = self.event.comments.count()
        self.assertEqual(response.status_code, HTTPStatus.OK, "Пользователь не авторизован")
        self.assertEqual(comments_count, 2, "Комментарий не добавлен")

    def test_event_add_comment_guest_client(self):
        """Проверка отправки комментария неавторизованным пользователем."""

        response = self.guest_client.post(reverse("events:events_comment", args=[self.event.id]), {"body": "test"})
        comments_count = self.event.comments.count()
        self.assertEqual(response.status_code, HTTPStatus.FOUND, "Пользователь не авторизован")
        self.assertEqual(comments_count, 1, "Комментарий не добавлен")

    def tearDown(self):
        Event.objects.all().delete()

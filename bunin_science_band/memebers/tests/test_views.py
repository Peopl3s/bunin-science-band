from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from http import HTTPStatus
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from memebers.models import Member

User = get_user_model()

MEMBERS_COUNT = 5
PAGINATE_COUNT = 3


# class PaginatorViewsTest(TestCase):
#     """Проверка пагинации участников."""

#     def setUp(self):
#         self.guest_client = Client()
#         self.user = User.objects.create_user(username="auth")
#         self.authorized_client = Client()
#         self.authorized_client.force_login(self.user)
#         bilk_members: list = []
#         for i in range(MEMBERS_COUNT):
#             bilk_members.append(
#                 Member(
#                     name=f"test{i}",
#                     surname=f"test{i}",
#                     midname="test",
#                     science_fields="test",
#                     rank=Member.Rank.PHD,
#                     phone=f"test{i}",
#                     email=f"test{i}",
#                     socials="test",
#                     description=f"test{i}",
#                     slug=f"test-doktor-nauk{i}",
#                     status=Member.Status.PUBLISHED,
#                 )
#             )
#         Member.objects.bulk_create(bilk_members)

#     def test_correct_page_context_guest_client(self):
#         """Проверка количества событий на первой и второй страницах."""

#         pages: tuple = (reverse("members:members_list"),)
#         for page in pages:
#             response1 = self.guest_client.get(page)
#             response2 = self.guest_client.get(page + "?page=2")
#             count_posts1 = len(response1.context["members"])
#             count_posts2 = len(response2.context["members"])

#             error_name1 = (
#                 f"Ошибка: {count_posts1} участников," f" должно быть{PAGINATE_COUNT}"
#             )
#             error_name2 = (
#                 f"Ошибка: {count_posts2} участников,"
#                 f"должно {MEMBERS_COUNT - PAGINATE_COUNT}"
#             )
#             self.assertEqual(count_posts1, PAGINATE_COUNT, error_name1)
#             self.assertEqual(count_posts2, MEMBERS_COUNT - PAGINATE_COUNT, error_name2)

# def test_correct_page_context_authorized_client(self):
#     """Проверка количества событий на первой и второй
#     страницах авторизованного пользователя."""

#     pages: tuple = (reverse("members:members_list"),)
#     for page in pages:
#         response1 = self.authorized_client.get(page)
#         response2 = self.authorized_client.get(page + "?page=2")
#         count_posts1 = len(response1.context["members"])
#         count_posts2 = len(response2.context["members"])

#         error_name1 = (
#             f"Ошибка: {count_posts1} участнков," f" должно быть{PAGINATE_COUNT}"
#         )
#         error_name2 = (
#             f"Ошибка: {count_posts2} участников,"
#             f"должно {MEMBERS_COUNT - PAGINATE_COUNT}"
#         )
#         self.assertEqual(count_posts1, PAGINATE_COUNT, error_name1)
#         self.assertEqual(count_posts2, MEMBERS_COUNT - PAGINATE_COUNT, error_name2)

# def tearDown(self):
#     Member.objects.all().delete()


class MembersViewsTests(TestCase):
    """Проверка предствлений участников."""

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username="auth", email="test@test.ru")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

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
            slug="test-doktor-nauk",
            status=Member.Status.PUBLISHED,
        )
        self.member.tags.add("test")

    def test_views_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""

        templates_url_names = {
            reverse("members:members_list"): "members/members/list.html",
            reverse(
                "members:members_list_by_tag",
                kwargs={"tag_slug": f"{self.member.tags.all()[0].slug}"},
            ): "members/members/list.html",
            reverse(
                "members:members_detail",
                args=[*self.member.get_absolute_url().split("/")[2:-1]],
            ): "members/members/detail.html",
        }
        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                error_name = f"Ошибка: {adress} ожидал шаблон {template}"
                self.assertTemplateUsed(response, template, error_name)

    # def test_member_added_correctly(self):
    #     """Участник при создании добавлена корректно."""

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
    #         slug="test-doktor-nauk",
    #         status=Member.Status.PUBLISHED,
    #     )

    #     member2 = Member.objects.create(
    #         name="test2",
    #         surname="test2",
    #         midname="test2",
    #         science_fields="test2",
    #         rank=Member.Rank.PHD,
    #         phone="test2",
    #         email="test2",
    #         socials="test2",
    #         description="test2",
    #         slug="test-doktor-nauk2",
    #         status=Member.Status.PUBLISHED,
    #     )
    #     member2.tags.add("test")

    #     response_index = self.authorized_client.get(reverse("members:members_list"))

    #     response_detail = self.authorized_client.get(
    #         reverse(
    #             "members:members_detail",
    #             args=[*member2.get_absolute_url().split("/")[2:-1]],
    #         )
    #     )

    #     response_tags = self.authorized_client.get(
    #         reverse(
    #             "members:members_list_by_tag",
    #             kwargs={"tag_slug": f"{member2.tags.all()[0].slug}"},
    #         )
    #     )

    #     index = response_index.context["members"]
    #     tags = response_tags.context["members"]
    #     detail = response_detail.context["members"]

    #     self.assertIn(member2, index, "Участника нет на главной")
    #     self.assertIn(member2, tags, "Участника нет в списке по тегам")
    #     self.assertEqual(member2, detail, "Участник не доступен для просмотра")

    def test_member_detail_page_show_correct_context(self):
        """Шаблон member_detail сформирован с правильным контекстом."""

        response = self.authorized_client.get(
            reverse(
                "members:members_detail",
                args=[*self.member.get_absolute_url().split("/")[2:-1]],
            )
        )
        post_text_0 = {
            response.context["members"].name: "test",
            response.context["members"].description: "test",
        }
        for value, expected in post_text_0.items():
            self.assertEqual(post_text_0[value], expected)

    def tearDown(self):
        Member.objects.all().delete()

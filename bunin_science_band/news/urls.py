from django.urls import path
from . import views
from .feeds import LatestPostsFeed
from likes.views import news_like

app_name = "news"

urlpatterns = [
    path("", views.news_list, name="news_list"),
    path("tag/<slug:tag_slug>/", views.news_list, name="news_list_by_tag"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:news>/",
        views.news_detail,
        name="news_detail",
    ),
    path("<int:news_id>/share/", views.news_share, name="news_share"),
    path("<int:news_id>/comment/", views.news_comment, name="news_comment"),
    path("feed/", LatestPostsFeed(5, 30), name="news_feed"),
    path("search/", views.news_search, name="news_search"),
    path(
        "comment/{<int:comment_id>}",
        views.news_comment_delete,
        name="news_comment_delete",
    ),
    path("news_like/{<int:news_id>}", news_like, name="news_like"),
]

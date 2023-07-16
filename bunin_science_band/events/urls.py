from django.urls import path
from . import views
from likes.views import event_like

app_name = "events"

urlpatterns = [
    path("", views.events_list, name="events_list"),
    path("tag/<slug:tag_slug>/", views.events_list, name="events_list_by_tag"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:events>/",
        views.events_detail,
        name="events_detail",
    ),
    path("<int:events_id>/share/", views.events_share, name="events_share"),
    path("<int:events_id>/comment/", views.events_comment, name="events_comment"),
    path("search/", views.events_search, name="events_search"),
    path(
        "comment/{<int:comment_id>}",
        views.events_comment_delete,
        name="events_comment_delete",
    ),
    path("events_like/{<int:event_id>}", event_like, name="events_like"),
]

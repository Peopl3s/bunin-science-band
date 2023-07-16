from django.urls import path
from . import views

app_name = "members"

urlpatterns = [
    path("", views.members_list, name="members_list"),
    path(
        "tag/<slug:tag_slug>/", views.members_list, name="members_list_by_tag"
    ),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:members>/",
        views.members_detail,
        name="members_detail",
    ),
]

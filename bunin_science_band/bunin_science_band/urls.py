from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from django.conf.urls import handler404, handler500
from .sitemaps import NewsSitemap, EventsSitemap, MembersSitemap

sitemaps = {
    "news": NewsSitemap,
    "events": EventsSitemap,
    "members": MembersSitemap,
}

urlpatterns = [
    path("account/", include("account.urls")),
    path("", include("home.urls")),
    path("admin/", admin.site.urls),
    path("news/", include("news.urls", namespace="news")),
    path("members/", include("memebers.urls", namespace="members")),
    path("events/", include("events.urls", namespace="events")),
    path("contacts/", include("info.urls", namespace="contacts")),
    re_path(
        r"^robots\.txt$",
        TemplateView.as_view(
            template_name="robots.txt", content_type="text/plain"
        ),
    ),
    re_path(
        r"^sitemap\.xml$",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]

handler404 = "home.views.page_not_found_view"
handler500 = "home.views.server_error_view"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

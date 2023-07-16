import logging
import viewer.services as viewer_services
import utils.list_helper as list_helper
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import redirect
from django.views.decorators.cache import cache_page
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from taggit.models import Tag
from . import services
from .models import News
from .forms import EmailNewsForm, CommentForm, SearchForm
from .tasks import share_by_email
from comments.models import Comment
from viewer.models import Viewer
from utils.core import transaction_safe_view


logger = logging.getLogger(__name__)


def news_search(request: HttpRequest) -> HttpResponse:
    """Вью для поиска по Новостям."""

    form = SearchForm()
    query = None
    results = []
    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            results = services.get_search_result_by_trigram(query, 0.1)
    return render(
        request,
        "news/news/search.html",
        {"form": form, "query": query, "results": results},
    )


@cache_page(1)
@transaction_safe_view
@require_POST
@login_required
def news_comment(request: HttpRequest, news_id: int) -> HttpResponse:
    """Вью для комментирования."""

    news = get_object_or_404(News, id=news_id, status=News.Status.PUBLISHED)
    comment = None
    # Комментарий был отправлен
    initial_dict = {"name": request.user.username, "email": request.user.email}
    form = CommentForm(data=request.POST, initial=initial_dict)
    if form.is_valid():
        # Создать объект класса Comment, не сохраняя его в базе данных
        comment = form.save(commit=False)
        # Назначить пост комментарию
        comment.news = news
        comment.events = None
        # Сохранить комментарий в базе данных
        comment.save()
    return render(
        request,
        "news/news/comment.html",
        {"news": news, "form": form, "comment": comment},
    )


@cache_page(1)
@transaction_safe_view
@login_required
def news_comment_delete(
    request: HttpRequest, comment_id: int
) -> HttpResponseRedirect:
    """Вью для удаления комментария."""

    comment = get_object_or_404(Comment, id=comment_id)
    news = comment.news
    logger.warning(
        f"Удалили комментарий {comment.name} : {comment.body} под новостью {news.title} - {news.get_absolute_url()}"
    )
    comment.delete()
    return redirect(news)


@login_required(login_url=settings.LOGIN_URL)
def news_share(request: HttpRequest, news_id: int) -> HttpResponse:
    """Вью чтобы поделиться новостью по email."""

    news = get_object_or_404(News, id=news_id, status=News.Status.PUBLISHED)
    sent = False
    if request.method == "POST":
        form = EmailNewsForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            news_url = request.build_absolute_uri(news.get_absolute_url())
            sent = share_by_email.delay(
                cd["name"],
                news.title,
                news_url,
                cd["comments"],
                settings.EMAIL_HOST_USER,
                cd["to"],
            )
    else:
        form = EmailNewsForm()
    return render(
        request,
        "news/news/share.html",
        {"news": news, "form": form, "sent": sent},
    )


def news_detail(
    request: HttpRequest, year: int, month: int, day: int, news: str
) -> HttpResponse:
    """Вью для отображения детальной информации о Новости."""

    news = get_object_or_404(
        News,
        status=News.Status.PUBLISHED,
        slug=news,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    # Список активных комментариев к этому посту
    client_ip = viewer_services.get_client_ip(
        request.META.get("HTTP_X_FORWARDED_FOR"),
        request.META.get("REMOTE_ADDR"),
    )
    viewer_services.add_view(news, client_ip)
    comments = list_helper.get_active_comments(news)
    form = None
    # Форма для комментирования пользователями
    if request.user.is_authenticated:
        form = CommentForm(
            initial={"name": request.user.username, "email": request.user.email}
        )
    news_tags_ids = list_helper.get_resource_tags_ids(news)
    similar_news = services.get_similar_news(news_tags_ids, news.id, 3)
    print(similar_news)
    return render(
        request,
        "news/news/detail.html",
        {
            "news": news,
            "comments": comments,
            "form": form,
            "similar_news": similar_news,
        },
    )


def news_list(request: HttpRequest, tag_slug: str = None) -> HttpResponse:
    """Вью для отображения списка Событий."""

    news_list = None
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        news_list = services.get_all_published_news_by_tag(tag)
    else:
        news_list = services.get_all_published_news()
    page_number = request.GET.get("page", 1)
    news = list_helper.get_paginated(news_list, page_number, 3)
    return render(request, "news/news/list.html", {"news": news, "tag": tag})

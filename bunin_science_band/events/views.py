from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.cache import cache_page
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from taggit.models import Tag
from .models import Event
from comments.models import Comment
from .forms import EmailEventForm, CommentForm, SearchForm
from . import services
import viewer.services as viewer_services
import utils.list_helper as list_helper
from utils.core import transaction_safe_view
from .tasks import share_by_email
import logging

logger = logging.getLogger(__name__)


@transaction_safe_view
@login_required(login_url=settings.LOGIN_URL)
def events_comment_delete(
    request: HttpRequest, comment_id: int
) -> HttpResponseRedirect:
    """Вью для удаления комментария."""

    comment = get_object_or_404(Comment, id=comment_id)
    event = comment.events
    logger.warning(
        f"Удалили комментарий {comment.name} : {comment.body} под событием {event.title} - {event.get_absolute_url()}"
    )
    comment.delete()
    return redirect(event)


def events_search(request: HttpRequest) -> HttpResponse:
    """Вью для поиска по Событиям."""

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
        "events/events/search.html",
        {"form": form, "query": query, "results": results},
    )


@cache_page(1)
@transaction_safe_view
@require_POST
@login_required(login_url=settings.LOGIN_URL)
def events_comment(request: HttpRequest, events_id: int) -> HttpResponse:
    """Вью для комментирования."""
    events = get_object_or_404(
        Event, id=events_id, status=Event.Status.PUBLISHED
    )
    comment = None
    # Комментарий был отправлен
    initial_dict = {"name": request.user.username, "email": request.user.email}
    form = CommentForm(data=request.POST, initial=initial_dict)
    if form.is_valid():
        # Создать объект класса Comment, не сохраняя его в базе данных
        comment = form.save(commit=False)
        # Назначить пост комментарию
        comment.events = events
        comment.news = None
        # Сохранить комментарий в базе данных
        comment.save()
    return render(
        request,
        "events/events/comment.html",
        {"events": events, "form": form, "comment": comment},
    )


@login_required(login_url=settings.LOGIN_URL)
def events_share(request: HttpRequest, events_id: int) -> HttpResponse:
    """Вью чтобы поделиться событием по email."""

    events = get_object_or_404(
        Event, id=events_id, status=Event.Status.PUBLISHED
    )
    sent = False
    if request.method == "POST":
        form = EmailEventForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            events_url = request.build_absolute_uri(events.get_absolute_url())
            sent = share_by_email.delay(
                cd["name"],
                events.title,
                events_url,
                cd["comments"],
                settings.EMAIL_HOST_USER,
                cd["to"],
            )
    else:
        form = EmailEventForm()
    return render(
        request,
        "events/events/share.html",
        {"events": events, "form": form, "sent": sent},
    )


def events_detail(
    request: HttpRequest, year: int, month: int, day: int, events: str
) -> HttpResponse:
    """Вью для отображения детальной информации о Событии."""

    events: Event = get_object_or_404(
        Event,
        status=Event.Status.PUBLISHED,
        slug=events,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    client_ip = viewer_services.get_client_ip(
        request.META.get("HTTP_X_FORWARDED_FOR"),
        request.META.get("REMOTE_ADDR"),
    )
    viewer_services.add_view(events, client_ip)
    # Список активных комментариев к этому посту
    comments = list_helper.get_active_comments(events)
    form = None
    if request.user.is_authenticated:
        form = CommentForm(
            initial={"name": request.user.username, "email": request.user.email}
        )
    events_tags_ids = list_helper.get_resource_tags_ids(events)
    similar_events = services.get_similar_events(events_tags_ids, events.id, 4)
    return render(
        request,
        "events/events/detail.html",
        {
            "events": events,
            "comments": comments,
            "form": form,
            "similar_events": similar_events,
        },
    )


def events_list(request: HttpRequest, tag_slug: str = None) -> HttpResponse:
    """Вью для отображения списка Событий."""

    # x = 1 / 0
    events_list = None
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        events_list = services.get_all_published_events_by_tag(tag)
    else:
        events_list = services.get_all_published_events()
    page_number = request.GET.get("page", 1)
    events = list_helper.get_paginated(events_list, page_number, 3)
    return render(
        request, "events/events/list.html", {"events": events, "tag": tag}
    )

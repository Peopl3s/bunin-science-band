from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from events.models import Event
from news.models import News
from . import services
from utils.core import transaction_safe_view
from django.contrib.auth.decorators import login_required


@login_required(login_url=settings.LOGIN_URL)
@transaction_safe_view
def event_like(request: HttpRequest, event_id: int) -> HttpResponse:
    """Добавляет/убирает лайк пользователя.
    Возвращает итоговое количество лайков.
    """

    event = get_object_or_404(Event, id=event_id)
    services.add_like(event, request.user.id)
    return JsonResponse({"likes_count": event.number_of_likes()}, status=200)


@login_required(login_url=settings.LOGIN_URL)
@transaction_safe_view
def news_like(request: HttpRequest, news_id: int) -> JsonResponse:
    """Добавляет/убирает лайк пользователя.
    Возвращает итоговое количество лайков.
    """

    news = get_object_or_404(News, id=news_id)
    services.add_like(news, request.user.id)
    return JsonResponse({"likes_count": news.number_of_likes()}, status=200)

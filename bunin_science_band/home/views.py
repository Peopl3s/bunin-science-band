from django.shortcuts import render
from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseServerError


def index(request: HttpRequest) -> HttpResponse:
    """Отдаёт гланую страницу сайта."""
    return render(request, "home/index.html")


def page_not_found_view(
    request: HttpRequest, exception: Exception
) -> HttpResponse:
    """Отдаёт кастомную страницу 404."""

    return render(
        request, f"{settings.ERRORS_TAMPLATES_PATH}/404.html", status=404
    )


def server_error_view(request: HttpRequest) -> HttpResponse:
    """Отдаёт кастомную страницу 500."""

    return render(
        request, f"{settings.ERRORS_TAMPLATES_PATH}/500.html", status=500
    )


def exp_500(request: HttpRequest) -> HttpResponse:
    """Вью для тестирования 500 ошибки ."""
    return HttpResponse(status=500)

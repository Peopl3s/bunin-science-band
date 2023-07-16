from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def contacts(request: HttpRequest) -> HttpResponse:
    """Отдаёт страницу с контактной информацией."""

    return render(request, "info/contacts.html")

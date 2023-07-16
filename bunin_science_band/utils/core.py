import functools
import inspect
from django.db import transaction
from django.http import HttpRequest
import typing


def transaction_safe_view(fn: typing.Callable) -> typing.Callable:
    """Декоратор для работы вью с транзакциями. Обеспечивает атомарность транзкций.

    Args:
        fn (callable): вызываемая функция
    Returns:
        callable: функция после воздействия декоратора
    """

    @functools.wraps(fn)
    def inner(
        request: HttpRequest, *args: list, **kwargs: dict
    ) -> typing.Callable:
        with transaction.atomic():
            return fn(request, *args, **kwargs)

    return inner

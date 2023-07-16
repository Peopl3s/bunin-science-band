import logging
import traceback
import typing
from django.http import JsonResponse
from django.http import HttpRequest, HttpResponse

logger = logging.getLogger(__name__)

JSON_DUMPS_PARAMS = {
    "ensure_ascii": False
}  # символы, не являющиеся ASCII, выведить как есть


class Process500:
    """Middleware для обраотки исключений и их логирования.

    Attributes:
        get_response (callable) : обработчик вызова
    Methods:
        __init__: Инициализирует обработчик.
        __call__: Возвращает ответ на запрос.
        process_exception: Обрабатывает и логирует любые исключения в проекте.
    """

    def __init__(self, get_response: typing.Callable) -> None:
        """Инициализирует обработчик."""

        self.__get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Возвращает ответ на запрос."""

        return self.__get_response(request)

    def process_exception(
        self, request: HttpRequest, exception: Exception
    ) -> JsonResponse:
        """Обрабатывает и логирует любые исключения в проекте."""

        logger.error(f"{str(exception)} - {traceback.format_exc()}")
        json_error_object = {"success": False, "error_message": str(exception)}
        return JsonResponse(
            json_error_object,
            json_dumps_params=JSON_DUMPS_PARAMS,
            status=400,
            safe=not isinstance(json_error_object, list),
        )

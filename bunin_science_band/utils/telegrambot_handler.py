import logging
import datetime
from typing import List


class TelegramFormatter(logging.Formatter):
    """Расширение обычного logging.Formatter для упрощения вида передаваемых данных.

    Attributes:
        meta_attrs (List[str]): список атрибутов с дополнительной информацией для лога
        limit (int): лимит стактреса https://docs.python.org/3/library/logging.html
    Methods:
        format: Форматирует сообщение лога.
    """

    meta_attrs = ["REMOTE_ADDR", "HOSTNAME", "HTTP_REFERER", "DATE_TIME"]
    limit = -1  # default per logging.Formatter is None

    def format(self, record: logging.LogRecord) -> str:
        """Аналогично logging.Formatter.format, с добавлением сообщения meta_attrs,
        когда они найдены в request.META.

        Args:
            record (str): сообщение для логирования
        Returns:
            str: отформатированный лог
        """

        info = super().format(record)

        info += "\n{attr}: {value}".format(
            attr="USER", value=record.request.user
        )
        info += "\n{attr}: {value}".format(
            attr="DATE_TIME",
            value=datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
        )

        for attr in self.meta_attrs:
            if attr in record.request.META:
                info += "\n{attr}: {value}".format(
                    attr=attr, value=record.request.META[attr]
                )
        return info


class TelegramHandler(logging.Handler):
    """Обработчик, который отправляет сообщение в Telegram для каждого события лога.

    Attributes:
    Methods:
        __init__: Инициализирует обработчик.
        _send_message: Обёртка для отправки сообщений ботом.
        emit: Форматирует и отправляет лог указанным адресатам.
    """

    def __init__(self, *args, **kwargs) -> None:
        """Инициализирует обработчик."""

        logging.Handler.__init__(self)
        if "token" in kwargs:
            self.token = kwargs["token"]
        if "mailing_list" in kwargs:
            self.mailing_list = kwargs["mailing_list"]
        if "bot" in kwargs:
            self.bot = kwargs["bot"]
        self.bot.token = self.token
        self.setFormatter(TelegramFormatter())

    def _send_message(self, msg: str, mailing_list: List[str | int]) -> None:
        """Обёртка для отправки сообщений ботом.
        Args:
            msg (str): сообщение для отправки.
            mailing_list (List[str|int]): список получателей сообщения - список id
        Returns:
        """

        for user in mailing_list:
            self.bot.send_message(user, msg, parse_mode="HTML")

    def emit(self, record: logging.LogRecord) -> None:
        """Форматирует и отправляет лог указанным адресатам.
        Args:
            record (str): сообщение для логирования
        Returns:
        """

        msg = self.format(record)
        self._send_message(msg, self.mailing_list)

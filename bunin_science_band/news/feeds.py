import markdown
from typing import List
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from django.db.models import DateTimeField
from .models import News


class LatestPostsFeed(Feed):
    """Класс для работы с RSS-фидом."""

    title = "Совет молодых учёных ЕГУ"
    link = reverse_lazy("news:news_list")
    description = "Новости Совета молодых учёных ЕГУ."

    def __init__(self, limit_news: int, limit_words: int) -> None:
        """Инициализирует лимит записей и длину сообщения."""

        self.limit_news = limit_news
        self.limit_words = limit_words

    def items(self) -> List[News]:
        """Возвращает опибликованные новости."""

        return list(News.published.all()[: self.limit_news])

    def item_title(self, item: News) -> str:
        """Возвращает заголовк новости."""

        return item.title

    def item_description(self, item: News) -> str:
        """Возвращает описание новости."""

        return truncatewords_html(
            markdown.markdown(item.body), self.limit_words
        )

    def item_pubdate(self, item: News) -> DateTimeField:
        """Возвращает дату и время публикации новости."""

        return item.publish

import logging
from typing import List, Optional
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from news.models import News
from events.models import Event
from comments.models import Comment
from memebers.models import Member

logger = logging.getLogger(__name__)


def get_paginated(
    resources: Optional[List[News | Event | Member]],
    page_number: int,
    paginate_limit: int,
) -> Optional[List[News | Event | Member]]:
    """Реализует пагинацию коллекции записей.
    Args:
        resources (List[News|Event|Member]): Коллекция основных сущностей сайта (Новости, События, Участники)
        page_number (int): номер текуще страницы пагинации
        paginate_limit (int): сколько записей выводить на 1 страницу пагинации
    Returns:
        List[News|Event|Member]: пагинированный список сущностей
    """

    paginator = Paginator(resources, paginate_limit)
    resources = None
    try:
        resources = paginator.page(page_number)
    except PageNotAnInteger:
        resources = paginator.page(1)
        logger.warning("Проблемы с пагинацией")
    except EmptyPage:
        resources = paginator.page(paginator.num_pages)
        logger.warning("Проблемы с пагинацией")
    return resources


def get_resource_tags_ids(resource: News | Event | Member) -> List[int]:
    """Получает список id тегов определённой записи.
    Args:
        resources (News|Event|Member): Сущность сайта (Новость, Событие, Участник)
    Returns:
        List[int]: список id тегов сущности
    """

    return list(resource.tags.values_list("id", flat=True))


def get_active_comments(resource: Event | News | Member) -> List[Comment]:
    """Получает список всех опубликованных комментариев под записью.
    Args:
        resource (News|Event|Member): Сущность сайта (Новость, Событие, Участник)
    Returns:
        List[Comment]: список активных комментариев под сущностью
    """

    comments = resource.comments.filter(active=True)
    return comments

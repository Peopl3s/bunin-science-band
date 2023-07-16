from typing import List
from django.db.models import Count
from django.contrib.postgres.search import TrigramSimilarity
from django.core.cache import cache
from django.db.models.query import QuerySet
from taggit.models import Tag
from .models import News


def get_similar_news(
    news_tags_ids: List[int], news_id: int, limit: int
) -> List[News]:
    """Возвращает список похожих (по количеству общих тегов) Новостей."""

    similar_news = cache.get("similar_news")
    if not similar_news:
        similar_news = News.published.filter(tags__in=news_tags_ids).exclude(
            id=news_id
        )
        similar_news = similar_news.annotate(same_tags=Count("tags")).order_by(
            "-same_tags", "-publish"
        )[:limit]
        cache.set("similar_news", similar_news)
    return list(similar_news)


def get_all_published_news() -> QuerySet:
    """Возвращает список всех опубликованных на сайте Новостей."""

    all_published_news = cache.get("all_published_news")
    if not all_published_news:
        all_published_news = News.published.all()
        cache.set("all_published_news", all_published_news)
    return all_published_news


def get_all_published_news_by_tag(tag: Tag) -> List[News]:
    """Возвращает список всех опубликованных на сайте Новостей по тегу."""

    return list(get_all_published_news().filter(tags__in=[tag]))


def get_search_result_by_trigram(query: str, coef: float) -> List[News]:
    """Возвращает список Новостей, удовлетворящих поисковому запросу."""

    searched_news = cache.get("searched_news")
    if not searched_news:
        # need CREATE EXTENSION pg_trgm;
        searched_news = (
            News.published.annotate(
                similarity=TrigramSimilarity("title", query),
            )
            .filter(similarity__gt=coef)
            .order_by("-similarity")
        )
        cache.set("searched_news", searched_news)
    return searched_news

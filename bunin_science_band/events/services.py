from typing import List
from django.db.models import Count
from django.contrib.postgres.search import TrigramSimilarity
from django.core.cache import cache
from taggit.models import Tag
from .models import Event


def get_similar_events(
    events_tags_ids: List[int], event_id: int, limit: int
) -> List[Event]:
    """Возвращает список похожих (по количеству общих тегов) Событий."""

    similar_events = cache.get("similar_events")
    if not similar_events:
        similar_events = Event.published.filter(
            tags__in=events_tags_ids
        ).exclude(id=event_id)
        similar_events = similar_events.annotate(
            same_tags=Count("tags")
        ).order_by("-same_tags", "-publish")[:limit]
        cache.set("similar_events", similar_events)
    return list(similar_events)


def get_all_published_events():
    """Возвращает список всех опубликованных на сайте Событий."""

    all_published_events = cache.get("all_published_events")
    if not all_published_events:
        all_published_events = Event.published.all()
        cache.set("all_published_events", all_published_events)
    return all_published_events


def get_all_published_events_by_tag(tag: Tag) -> List[Event]:
    """Возвращает список всех опубликованных на сайте Событий по тегу."""

    return list(get_all_published_events().filter(tags__in=[tag]))


def get_search_result_by_trigram(query: str, coef: float) -> List[Event]:
    """Возвращает список Событий, удовлетворящих поисковому запросу."""

    searched_events = cache.get("searched_events")
    if not searched_events:
        searched_events = (
            Event.published.annotate(
                similarity=TrigramSimilarity("title", query),
            )
            .filter(similarity__gt=coef)
            .order_by("-similarity")
        )
        cache.set("searched_events", searched_events)
    return searched_events

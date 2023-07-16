from typing import List
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.core.cache import cache
from taggit.models import Tag
from .models import Member


def get_members_tags_ids(member: Member) -> List[int]:
    """Возвращает список id тегов конретного участника."""

    all_members_tags_ids = cache.get("all_members_tags_ids")
    if not all_members_tags_ids:
        all_members_tags_ids = member.tags.values_list("id", flat=True)
        cache.set("all_members_tags_ids", all_members_tags_ids)
    return list(all_members_tags_ids)


def get_similar_members(
    members_tags_ids: List[int], member_id: int, limit: int
) -> List[Member]:
    """Возвращает список похожих (по количеству общих тегов) участников."""

    similar_members = cache.get("similar_members")
    if not similar_members:
        similar_members = Member.published.filter(
            tags__in=members_tags_ids
        ).exclude(id=member_id)
        similar_members = similar_members.annotate(
            same_tags=Count("tags")
        ).order_by("-same_tags", "-publish")[:limit]
        cache.set("similar_members", similar_members)
    return list(similar_members)


def get_all_published_members():
    """Возвращает список всех опубликованных на сайте участников."""

    all_published_members = cache.get("all_published_members")
    if not all_published_members:
        all_published_members = Member.published.all()
        cache.set("all_published_members", all_published_members)
    return all_published_members


def get_all_published_members_by_tag(tag: Tag) -> List[Member]:
    """Возвращает список всех опубликованных на сайте участников по тегу."""

    return list(get_all_published_members().filter(tags__in=[tag]))

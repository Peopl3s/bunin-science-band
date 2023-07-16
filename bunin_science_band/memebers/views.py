from typing import List
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest
from taggit.models import Tag
import utils.list_helper as list_helper
from .models import Member
from . import services


def members_detail(
    request: HttpRequest, year: int, month: int, day: int, members: str
) -> HttpResponse:
    """Вью для отображения детальной информации об участнике."""
    member = get_object_or_404(
        Member,
        status=Member.Status.PUBLISHED,
        slug=members,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    members_tags_ids: List[int] = services.get_members_tags_ids(member)
    similar_members: List[Member] = services.get_similar_members(
        members_tags_ids, member.id, 4
    )
    return render(
        request,
        "members/members/detail.html",
        {"members": member, "similar_members": similar_members},
    )


def members_list(request: HttpRequest, tag_slug: str = None) -> HttpResponse:
    """Вью для отображения списка участников."""

    members_list = None
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        members_list = services.get_all_published_members_by_tag(tag)
    else:
        members_list = services.get_all_published_members()
    page_number: int = request.GET.get("page", 1)
    members: List[Member] = list_helper.get_paginated(
        members_list, page_number, 3
    )
    return render(
        request, "members/members/list.html", {"members": members, "tag": tag}
    )

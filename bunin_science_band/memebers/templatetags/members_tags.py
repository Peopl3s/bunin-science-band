from django import template
from ..models import Member
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()


@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.simple_tag
def total_members():
    return Member.published.count()

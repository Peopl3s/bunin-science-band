from django import template
from ..models import Member
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
import os

register = template.Library()


@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.simple_tag
def total_members():
    return Member.published.count()


@register.filter
def ru_plural(value, variants):
    variants = variants.split(",")
    value = abs(int(value))

    if value % 10 == 1 and value % 100 != 11:
        variant = 0
    elif (
        value % 10 >= 2 and value % 10 <= 4 and (value % 100 < 10 or value % 100 >= 20)
    ):
        variant = 1
    else:
        variant = 2

    return variants[variant]


@register.filter
def filename(value):
    return os.path.basename(value.file.name)

from django import template
from ..models import News
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()


@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.simple_tag
def total_news():
    return News.published.count()


@register.inclusion_tag("news/news/latest_news.html")
def show_latest_news(count=5):
    latest_news = News.published.order_by("-publish")[:count]
    return {"latest_news": latest_news}


@register.simple_tag
def get_most_commented_news(count=5):
    return News.published.annotate(total_comments=Count("comments")).order_by(
        "-total_comments"
    )[:count]


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

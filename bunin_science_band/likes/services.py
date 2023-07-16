from news.models import News
from events.models import Event


def add_like(resource: News | Event, user_id: int) -> None:
    """Добавляет/удаляет лайк на запись."""

    if resource.likes.filter(id=user_id).exists():
        resource.likes.remove(user_id)
    else:
        resource.likes.add(user_id)

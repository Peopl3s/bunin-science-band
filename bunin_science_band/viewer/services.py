from news.models import News
from events.models import Event
from .models import Viewer


def get_client_ip(x_forwarded_for: str, remote_addr: str) -> str:
    """Получает ip адрес."""

    return (
        x_forwarded_for.split(",")[-1].strip()
        if x_forwarded_for
        else remote_addr
    )


def add_view(resource: News | Event, client_ip: str) -> None:
    """Добавляет просмотр на запись."""

    view = None
    if not Viewer.objects.filter(ipaddress=client_ip).exists():
        view = Viewer.objects.create(ipaddress=client_ip)
    if not view:
        view = Viewer.objects.get(ipaddress=client_ip)
    resource.viewes.add(view)

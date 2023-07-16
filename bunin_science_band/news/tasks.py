from django.core.mail import send_mail
from celery import shared_task


@shared_task
def share_by_email(
    name: str,
    title: str,
    url: str,
    comment: str,
    from_user: str,
    to: str,
) -> bool:
    """Отправляет email с рекомендацией прочитать запись."""

    subject = f"{name} рекомменудет вам почитать {title}"
    message = f"Почитайте {title} по адресу {url}\n {name}:" f"{comment}"
    return send_mail(subject, message, from_user, [to], fail_silently=False)

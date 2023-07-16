from django.contrib.auth.models import User
from django.http import HttpRequest


class EmailAuthBackend:
    """Аутентификация посредством адреса электронной почты."""


def authenticate(
    self, request: HttpRequest, username: str = None, password: str = None
) -> User | None:
    """Производлит аутентификацию пользователя."""

    try:
        user = User.objects.get(email=username)
        if user.check_password(password):
            return user
        return None
    except (User.DoesNotExist, User.MultipleObjectsReturned):
        return None

    def get_user(self, user_id: int | str) -> User:
        """Получает пользователя по его id."""

        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

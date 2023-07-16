from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from utils.core import transaction_safe_view
from .forms import LoginForm, UserRegistrationForm, UserEditForm
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.shortcuts import resolve_url


@transaction_safe_view
@login_required
def edit(request: HttpRequest) -> HttpResponse:
    """Вью для редактирования данных пользователя."""

    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Профиль успешно обновлён")
        else:
            messages.error(request, "Ошибка обновления профиля")
    else:
        user_form = UserEditForm(instance=request.user)
    return render(
        request, "account/account/edit.html", {"user_form": user_form}
    )


@transaction_safe_view
def register(request: HttpRequest) -> HttpResponse:
    """Вью для регистрации пользователя."""

    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создать новый объект пользователя,
            # но пока не сохранять его
            new_user = user_form.save(commit=False)
            # Установить выбранный пароль
            new_user.set_password(user_form.cleaned_data["password"])
            # Сохранить объект User
            new_user.save()
            return render(
                request,
                "account/account/register_done.html",
                {"new_user": new_user},
            )
    else:
        user_form = UserRegistrationForm()
    return render(
        request, "account/account/register.html", {"user_form": user_form}
    )


def user_login(request: HttpRequest) -> HttpResponse:
    """Вью для аутентификации пользователя."""

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd["username"], password=cd["password"]
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return reverse(settings.LOGIN_REDIRECT_URL)
                else:
                    return reverse(settings.LOGIN_URL)
            else:
                return reverse(settings.LOGIN_URL)
    else:
        form = LoginForm()
    return render(request, "account/registration/login.html", {"form": form})


# class LoginView(auth_views.LoginView):
#     template_name = "account/registration/login.html"

#     def get_success_url(self):
#         return resolve_url(settings.LOGIN_REDIRECT_URL)


# class LogoutView(auth_views.LogoutView):
#     template_name = "account/registration/logged_out.html"

#     def get_success_url(self):
#         return resolve_url(settings.LOGIN_URL)
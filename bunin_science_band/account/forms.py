from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.conf import settings

class LoginForm(forms.Form):
    """Форма авторизации (входа)."""

    username = forms.CharField(
        label="Имя пользователя",
    )
    email = forms.EmailField(label="Email", max_length=200)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    """Форма регистрации (входа)."""

    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Повторите пароль", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def clean_password(self):
        """Проверяет пароль на соответствие требованиям."""

        password = self.cleaned_data["password"]
        try:
            validate_password(password)
        except forms.ValidationError as error:
            self.add_error("password", error)
        return password

    def clean_password2(self) -> str:
        """Проверяет совпадает ли значение поля Пароль и Подтверждение пароля."""

        cd = self.cleaned_data

        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Пароль не совпадает.")
        return cd["password2"]

    def clean_email(self) -> str:
        """Проверяет зарегистрирован ли пользователь с такой почтой."""

        data = self.cleaned_data["email"]
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("Email уже используется.")
        return data


class UserEditForm(forms.ModelForm):
    """Форма редактирования данных пользователя."""

    class Meta:
        model = User
        fields = ["username", "email"]

    def clean_email(self) -> str:
        """Проверяет уникальность почты."""
        data = self.cleaned_data["email"]
        qs = User.objects.exclude(id=self.instance.id).filter(email=data)
        if qs.exists():
            raise forms.ValidationError(" Email already in use.")
        return data

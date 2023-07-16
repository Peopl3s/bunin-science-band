from django import forms
from comments.models import Comment


class EmailEventForm(forms.Form):
    """Форма для отправки События по email (репост события)."""

    name = forms.CharField(max_length=25, label="Имя")
    to = forms.EmailField(label="Кому (email)")
    comments = forms.CharField(
        required=False, widget=forms.Textarea, label="Комментарий"
    )


class CommentForm(forms.ModelForm):
    """Форма для отправки комментария под записью События."""

    email = forms.EmailField(disabled=True, label="Email")
    name = forms.CharField(disabled=True, label="Имя")

    class Meta:
        model = Comment
        fields = ["name", "email", "body"]


class SearchForm(forms.Form):
    """Форма поиска по событиям."""

    query = forms.CharField(label="Запрос")

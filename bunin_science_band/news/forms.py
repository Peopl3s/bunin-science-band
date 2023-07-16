from django import forms
from comments.models import Comment


class EmailNewsForm(forms.Form):
    """Форма для отправки Новости по email (репост новости)."""

    name = forms.CharField(max_length=25, label="Имя")
    to = forms.EmailField(label="Кому")
    comments = forms.CharField(
        required=False, widget=forms.Textarea, label="Комментарий"
    )


class CommentForm(forms.ModelForm):
    """Форма для отправки комментария под записью Новостью."""

    email = forms.EmailField(disabled=True, label="Email")
    name = forms.CharField(disabled=True, label="Имя")

    class Meta:
        model = Comment
        fields = ["name", "email", "body"]


class SearchForm(forms.Form):
    """Форма поиска по Новостям."""

    query = forms.CharField(label="Запрос")

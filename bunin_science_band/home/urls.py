from django.urls import path, include
from . import views

app_name = "home"

urlpatterns = [
    path("", views.index, name="index"),
    path("500/", views.exp_500, name="exp_500"),
]

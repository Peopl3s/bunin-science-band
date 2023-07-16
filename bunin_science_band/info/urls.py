from django.urls import path, include
from . import views

app_name = "contacts"

urlpatterns = [
    path("", views.contacts, name="contacts"),
]

from django.urls import path
from . import views

app_name = "example"

urlpatterns = [
    path("unauthenticated/", views.unauthenticated_endpoint, name="unauthenticated"),
    path("authenticated/", views.authenticated_endpoint, name="authenticated"),
    path("settings/", views.settings_endpoint, name="settings"),
]

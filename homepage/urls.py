from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage_index, name="homepage_index"),
]
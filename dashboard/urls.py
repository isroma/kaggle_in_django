from django.urls import path
from . import views

urlpatterns = [
    path("actives", views.actives, name="actives"),
    path("coming", views.coming, name="coming"),
    path("pasts", views.pasts, name="pasts"),
    path("creating", views.creating, name="creating"),
    path("<int:pk>/", views.competition, name="competition"),
    path("delete/<int:pk>/", views.delete, name="delete"),
]
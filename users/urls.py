from django.urls import path
from . import views


urlpatterns = [
    path('login', views.login, name='login'),
    path('welcome', views.welcome, name='welcome'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('activate/<slug:uidb64>/<slug:token>', views.activate, name='activate'),
]
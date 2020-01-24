from django.urls import path
from kunder import views

urlpatterns = [
    path("", views.home, name="home"),
]

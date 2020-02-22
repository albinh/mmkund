from django.urls import path
from kunder import views

urlpatterns = [
    path("", views.home, name="home"),
    path("minaleveranser", views.my_deliveries, name="minaleveranser"),
    path("logga-in-kund", views.login_customer, name="loggainkund")
]

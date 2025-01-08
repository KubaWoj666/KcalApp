from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("add-product/", views.add_and_fetch_product, name="add_product")
]
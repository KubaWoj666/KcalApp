from django.urls import path
from . import views

urlpatterns = [
    path("cal/", views.CalendarView.as_view(), name="calendar"),
    path("delete-meal/", views.delete_meal_entry, name="delete-meal")
]
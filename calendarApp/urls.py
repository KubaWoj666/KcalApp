from django.urls import path
from . import views

urlpatterns = [
    path("cal/", views.CalendarView.as_view(), name="calendar"),
    path("delete-meal/", views.delete_meal_entry, name="delete-meal"),
    path("add-snack-entry/", views.add_snack_entry, name="add_snack_entry"),
    path("delete-snack/", views.delete_snack_entry, name="delete_snack"),
]
from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.CustomSignupView.as_view(), name="account_signup"),
    path("profile-create/<uuid:pk>/", views.finish_profile_create, name="profile_create"),
    path("profile/<uuid:pk>/", views.profile, name="profile"),
    path("recipe/<int:recipe_id>/delete", views.delete_recipe_view, name="delete_recipe")
]
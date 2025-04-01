from django.urls import path

from . import views

urlpatterns = [
    # path("", views.create_user_view, name="create_user"),
    # path("login/", views.login_user, name="login"),
    # path("logout/", views.logout_user, name="logout"),
    path("signup/", views.CustomSignupView.as_view(), name="account_signup"),
    # path("social/signup/", views.CustomSocialSignupView.as_view(), name="socialaccount_signup"),
    path("profile-create/<uuid:pk>/", views.finish_profile_create, name="profile_create"),
    path("profile/<uuid:pk>/", views.profile, name="profile"),
]
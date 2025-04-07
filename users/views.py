from django.shortcuts import render, redirect, resolve_url
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm

from core.models import Recipe

from .models import UserAccount
from .forms import CustomUserCreationForm
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout

from allauth.account.views import SignupView
from allauth.socialaccount.views import SignupView as SocialSignupView
from .models import UserAccount
from django.shortcuts import get_object_or_404, get_list_or_404

from allauth.account.adapter import DefaultAccountAdapter
 
class MyAccountAdapter(DefaultAccountAdapter):

    def get_signup_redirect_url(self, request):
        return  reverse("profile_create", kwargs={"pk": request.user.id})


class CustomSignupView(SignupView):
    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.user
        return redirect("profile_create", pk=user.id)
    

def finish_profile_create(request, pk):
    user = get_object_or_404(UserAccount, id=pk)
    form = CustomUserCreationForm()

    if request.method == "POST":
        print("post")
        form = CustomUserCreationForm(request.POST or None, instance=user)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect("profile", pk=user.id)

    context = {
        "user": user,
        "form": form,
    } 

    return render(request, "users/finish_profile.html", context)


def profile(request, pk):
    user = get_object_or_404(UserAccount, pk=request.user.id)
    recipes = get_list_or_404(Recipe, creator=user)

    context = {
        "user": user,
        "recipes": recipes
    }
    return render(request, "users/profile.html", context)


# def create_user_view(request):
#     form = CustomUserCreationForm()

#     login_form = AuthenticationForm()

#     if request.method == "POST":
#         print("post")
#         form = CustomUserCreationForm(request.POST or None)
#         if form.is_valid():
#             print("valid")
#             form.save()
#             return redirect("home")

#     context = {
#         "form": form,
#         "login_form": login_form
#     }

#     return render(request, "users/create_user.html", context)


# def login_user(request):
#     form = AuthenticationForm()
#     if request.method == "POST":
#         form = AuthenticationForm(request, data=request.POST)  # Ważne: przekazujemy `request`
#         if form.is_valid():
#             email = form.cleaned_data.get("username")  # Django oczekuje pola `username`
#             password = form.cleaned_data.get("password")

#             user = authenticate(request, username=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect("home")
#     else:
#         print("Nieprawidłowe dane logowania")
    
#     context = {
#         "form": form
#     }
#     return render(request, "users/login.html", context )


# def logout_user(request):
#     print(request.method)
#     logout(request)
#     return redirect("home")


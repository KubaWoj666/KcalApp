from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm

from .models import UserAccount
from .forms import CustomUserCreationForm
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout


def create_user_view(request):
    form = CustomUserCreationForm()

    login_form = AuthenticationForm()

    if request.method == "POST":
        print("post")
        form = CustomUserCreationForm(request.POST or None)
        if form.is_valid():
            print("valid")
            form.save()
            return redirect("home")

    context = {
        "form": form,
        "login_form": login_form
    }

    return render(request, "users/create_user.html", context)


def login_user(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)  # Ważne: przekazujemy `request`
        if form.is_valid():
            email = form.cleaned_data.get("username")  # Django oczekuje pola `username`
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
    else:
        print("Nieprawidłowe dane logowania")
    
    context = {
        "form": form
    }
    return render(request, "users/login.html", context )


def logout_user(request):
    print(request.method)
    logout(request)
    return redirect("home")


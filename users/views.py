from django.shortcuts import render, redirect

from .models import UserAccount
from .forms import CustomUserCreationForm

def create_user_view(request):
    form = CustomUserCreationForm

    if request.method == "POST":
        print("post")
        form = CustomUserCreationForm(request.POST or None)
        if form.is_valid():
            print("valid")
            form.save()
            return redirect("home")

    context = {
        "form": form
    }

    return render(request, "users/create_user.html", context)
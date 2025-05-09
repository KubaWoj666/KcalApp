from django.shortcuts import render, redirect, resolve_url
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
import datetime
from django.db.models import Sum, F
from django.utils import timezone

from core.models import Recipe, MealEntry
from django_htmx.http import HttpResponseClientRefresh


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
    recipes = Recipe.objects.filter(creator=user)

    daily = MealEntry.objects.filter(date=datetime.date.today()).aggregate(
    kcal=Sum(F("meal__kcal")),
    protein=Sum(F("meal__protein")),
    carbs=Sum(F("meal__carbs")),
    fat=Sum(F("meal__fat")),
    )
    
    some_day_last_week = datetime.date.today() - datetime.timedelta(days=7)
    some_day_last_week_SO = timezone.now().date() - datetime.timedelta(days=7)
    monday_of_last_week = some_day_last_week - datetime.timedelta(days=(some_day_last_week.isocalendar()[2] - 1))
    monday_of_this_week = monday_of_last_week + datetime.timedelta(days=7)


    last_week = MealEntry.objects.filter(date__gte=monday_of_last_week, date__lt=monday_of_this_week).aggregate(
    kcal=Sum(F("meal__kcal")),
    protein=Sum(F("meal__protein")),
    carbs=Sum(F("meal__carbs")),
    fat=Sum(F("meal__fat")),
    )

    date = datetime.date.today()
    start_week = date - datetime.timedelta(date.weekday())
    end_week = start_week + datetime.timedelta(7)

    current_week = MealEntry.objects.filter(date__gte=start_week, date__lt=end_week).aggregate(
    kcal=Sum(F("meal__kcal")),
    protein=Sum(F("meal__protein")),
    carbs=Sum(F("meal__carbs")),
    fat=Sum(F("meal__fat")),
    )

    context = {
        "user": user,
        "recipes": recipes,
        "daily": daily,  
        "current_week": current_week,
        "last_week": last_week    
    }
    return render(request, "users/profile.html", context)


def delete_recipe_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, creator=request.user)
    recipe.delete()
    return redirect("profile", request.user.id)

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


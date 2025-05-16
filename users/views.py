import datetime

from django_htmx.http import HttpResponseClientRefresh
from django.shortcuts import  get_object_or_404, redirect, render
from django.urls import reverse



from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.views import SignupView

from core.models import Recipe

from .forms import CustomUserCreationForm, WeighEntryForm
from .models import UserAccount
from .utils import aggregate_nutrition


 
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
    user = get_object_or_404(UserAccount, id=pk)
    recipes = Recipe.objects.filter(creator=user)
    form = WeighEntryForm(user=user)

    # Aggregate nutrition data for today
    daily_nutrition = aggregate_nutrition(user, today=datetime.date.today())

    # Calculate current week range (Monday to Sunday)
    date = datetime.date.today()
    start_week = date - datetime.timedelta(date.weekday())
    end_week = start_week + datetime.timedelta(7)

    # Aggregate nutrition data for the current week
    current_week_nutrition = aggregate_nutrition(user, date_from=start_week, date_to=end_week)
    
    # Calculate last week range
    some_day_last_week = datetime.date.today() - datetime.timedelta(days=7)
    monday_of_last_week = some_day_last_week - datetime.timedelta(days=(some_day_last_week.isocalendar()[2] - 1))
    monday_of_this_week = monday_of_last_week + datetime.timedelta(days=7)

    # Aggregate nutrition data for the previous week
    last_week_nutrition = aggregate_nutrition(user, date_from=monday_of_last_week, date_to=monday_of_this_week)

    if request.method == "POST":
        form = WeighEntryForm(request.POST or None, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile", user.id)


    context = {
        "user": user,
        "recipes": recipes,
        "form": form,
        "daily": daily_nutrition,  
        "current_week": current_week_nutrition,
        "last_week": last_week_nutrition    
    }
    return render(request, "users/profile.html", context)





def delete_recipe_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, creator=request.user)
    recipe.delete()
    return redirect("profile", request.user.id)


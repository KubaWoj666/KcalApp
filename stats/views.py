from django.shortcuts import render
from .forms import StatsForm
from core.models import MealEntry, Meal
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib

import json

from .utils import get_plot




matplotlib.use("Agg")
def index_stats(request):
    form = StatsForm()
    df = None
    totals = {}
    date_from = None
    date_to = None
    meal_entry_df = None
    chart = None
    chart_kcal = None
    chart_protein = None
    chart_carbs = None
    chart_fat = None

    if request.method == "POST":
        form = StatsForm(request.POST or None)
        if form.is_valid():
            date_from = form.cleaned_data.get("date_from")
            date_to = form.cleaned_data.get("date_to")

            meal_entry_qs = MealEntry.objects.filter(date__gte=date_from, date__lte=date_to).order_by("date")
            
            if len(meal_entry_qs) > 0:
                meal_entry_df = pd.DataFrame(meal_entry_qs.values())
                meal_entry_df["date"] = meal_entry_df["date"].apply(lambda x: x.strftime("%d-%m-%Y"))
                meal_entry_df.columns = meal_entry_df.columns.str.replace("id", "meal")
                meal_entry_df["kcal"] = meal_entry_df["meal_meal"].apply(lambda meal_id: Meal.objects.get(id=meal_id).kcal)
                meal_entry_df["protein"] = meal_entry_df["meal_meal"].apply(lambda meal_id: Meal.objects.get(id=meal_id).protein)
                meal_entry_df["carbs"] = meal_entry_df["meal_meal"].apply(lambda meal_id: Meal.objects.get(id=meal_id).carbs)
                meal_entry_df["fat"] = meal_entry_df["meal_meal"].apply(lambda meal_id: Meal.objects.get(id=meal_id).fat)

                meal_entry_df["kcal"] *= meal_entry_df["portions"]
                meal_entry_df["protein"] *= meal_entry_df["portions"]
                meal_entry_df["fat"] *= meal_entry_df["portions"]
                meal_entry_df["carbs"] *= meal_entry_df["portions"]

                meal_entry_df["meal"] = meal_entry_df["meal_meal"].apply(get_meal_name)
                meal_entry_df = meal_entry_df.drop("meal_meal", axis=1)
                for entry in meal_entry_qs:
                    totals["kcal"] = totals.get("kcal", 0) + entry.meal.kcal
                    totals["protein"] = totals.get("protein", 0) + entry.meal.protein
                    totals["carbs"] = totals.get("carbs", 0) + entry.meal.carbs
                    totals["fat"] = totals.get("fat", 0) + entry.meal.fat 
                
                df = meal_entry_df.groupby("date").agg({
                    "kcal": "sum",
                    "protein": "sum",
                    "carbs": "sum",
                    "fat": "sum",
                })
                json_records = df.reset_index().to_json(default_handler=str, orient='records')
                data = json.loads(json_records)
                print(1)
                chart = get_plot(date_from, date_to, data,nutrition=None, df=df )
                print(2)
                chart_kcal = get_plot(date_from, date_to, data,nutrition="kcal", df=None)
                print(3)
                chart_protein = get_plot(date_from, date_to, data,nutrition="protein", df=None)
                chart_carbs = get_plot(date_from, date_to, data,nutrition="carbs", df=None)
                chart_fat = get_plot(date_from, date_to, data,nutrition="fat", df=None)
               
                                
                meal_entry_df = meal_entry_df.to_html(index=False, classes="table table-striped table-bordered", border=0)


    context = {
        "form": form,
        "meal_entry_df": meal_entry_df,
        "totals": totals,
        "date_from": date_from,
        "date_to": date_to,
        "chart": chart,
        "chart_kcal": chart_kcal,
        "chart_protein": chart_protein,
        "chart_carbs": chart_carbs,
        "chart_fat": chart_fat
    }

    return render(request, "stats/stats.html", context)


def get_meal_name(meal_meal):
    meal = Meal.objects.get(id=meal_meal)
    return meal.recipe

    
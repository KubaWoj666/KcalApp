from django.shortcuts import render
from .forms import StatsForm
from core.models import MealEntry, SnackEntry
import pandas as pd
from decimal import Decimal
import json
from .utils import get_plot
import matplotlib
matplotlib.use("Agg")

def index_stats(request):
    user = request.user
    form = StatsForm()
    meal_entry_df = None
    totals = {}
    chart = chart_kcal = chart_protein = chart_carbs = chart_fat = None
    date_from = date_to = None
    meal_data = []
    snack_data = []

    if request.method == "POST":
        form = StatsForm(request.POST)
        if form.is_valid():
            date_from = form.cleaned_data["date_from"]
            date_to = form.cleaned_data["date_to"]

            meal_entry_qs = MealEntry.objects.filter(
                date__gte=date_from, date__lte=date_to, meal__creator=user
            ).order_by("date")

            snack_entry_qs = SnackEntry.objects.filter(
                date__gte=date_from, date__lte=date_to, product__creator=user
            ).order_by("date")

            # Zbieranie danych
            for entry in meal_entry_qs:
                meal_data.append({
                    "date": entry.date.strftime("%d-%m-%Y"),
                    "kcal": entry.meal.kcal * entry.portions,
                    "protein": entry.meal.protein * entry.portions,
                    "carbs": entry.meal.carbs * entry.portions,
                    "fat": entry.meal.fat * entry.portions,
                })
                totals["kcal"] = totals.get("kcal", 0) + (entry.meal.kcal * entry.portions)
                totals["protein"] = totals.get("protein", 0) + (entry.meal.protein * entry.portions)
                totals["carbs"] = totals.get("carbs", 0) + (entry.meal.carbs * entry.portions)
                totals["fat"] = totals.get("fat", 0) + (entry.meal.fat * entry.portions)

            for entry in snack_entry_qs:
                kcal = entry.product.kcal * Decimal(entry.grams) / 100
                protein = entry.product.protein * Decimal(entry.grams) / 100
                carbs = entry.product.carbs * Decimal(entry.grams) / 100
                fat = entry.product.fat * Decimal(entry.grams) / 100
                snack_data.append({
                    "date": entry.date.strftime("%d-%m-%Y"),
                    "kcal": kcal,
                    "protein": protein,
                    "carbs": carbs,
                    "fat": fat,
                })
                totals["kcal"] += kcal
                totals["protein"] += protein
                totals["carbs"] += carbs
                totals["fat"] += fat

            if meal_data or snack_data:
                all_data_df = pd.DataFrame(meal_data + snack_data)
                daily_summary_df = all_data_df.groupby("date").agg({
                    "kcal": "sum",
                    "protein": "sum",
                    "carbs": "sum",
                    "fat": "sum"
                }).reset_index().round(2)

                df = daily_summary_df.set_index("date")
                json_records = df.reset_index().to_json(default_handler=str, orient='records')
                data = json.loads(json_records)

                chart = get_plot(date_from, date_to, data, nutrition=None, df=df)
                chart_kcal = get_plot(date_from, date_to, data, nutrition="kcal", df=None)
                chart_protein = get_plot(date_from, date_to, data, nutrition="protein", df=None)
                chart_carbs = get_plot(date_from, date_to, data, nutrition="carbs", df=None)
                chart_fat = get_plot(date_from, date_to, data, nutrition="fat", df=None)

                meal_entry_df = daily_summary_df.to_html(index=False, classes="table table-striped table-bordered", border=0)

    context = {
        "form": form,
        "meal_entry_df": meal_entry_df,
        "totals": {k: round(v, 2) for k, v in totals.items()},
        "date_from": date_from,
        "date_to": date_to,
        "chart": chart,
        "chart_kcal": chart_kcal,
        "chart_protein": chart_protein,
        "chart_carbs": chart_carbs,
        "chart_fat": chart_fat
    }

    return render(request, "stats/stats.html", context)

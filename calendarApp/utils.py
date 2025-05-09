from datetime import datetime, timedelta
from calendar import HTMLCalendar, monthrange
from core.models import MealEntry, SnackEntry


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None, request=None):
        super().__init__()
        self.year = year
        self.month = month
        self.today = datetime.today().date()
        self.request = request

    def formatday(self, day, meal_entries, snack_entries):
        user = self.request.user
        if day == 0:
            return "<td></td>"

        days_in_month = monthrange(self.year, self.month)[1]
        if day > days_in_month:
            return "<td></td>"

        meals_per_day = meal_entries.filter(date__day=day)
        snacks_per_day = snack_entries.filter(date__day=day, user=user)

        total_kcal = total_protein = total_fat = total_carbs = 0
        meal_list = ""

        for meal in meals_per_day:
            total_kcal += meal.meal.kcal * meal.portions
            total_protein += meal.meal.protein * meal.portions
            total_fat += meal.meal.fat * meal.portions
            total_carbs += meal.meal.carbs * meal.portions
            meal_list += (
                f"<li>{meal.get_html_url} ({meal.portions}x) "
                f"<form method='POST' action='/cal/delete-meal/' class='delete-meal-form'>"
                f"    <input type='hidden' name='csrfmiddlewaretoken' value=''>"
                f"    <input type='hidden' name='meal_id' value='{meal.meal.id}'>"
                f"    <input type='hidden' name='meal_entry' value='{meal.id}'>"
                f"    <input type='hidden' name='date' value='{self.year}-{self.month}-{day}'>"
                f"    <button type='submit' class='delete-button'><i class='fa-solid fa-x'></i></button>"
                f"</form></li>"
            )

        for snack in snacks_per_day:
            total_kcal += snack.product.kcal * snack.grams / 100
            total_protein += snack.product.protein * snack.grams / 100
            total_fat += snack.product.fat * snack.grams / 100
            total_carbs += snack.product.carbs * snack.grams / 100
            meal_list += (
                f"<li>{snack.product.name} ({snack.grams}g) "
                f"<form method='POST' action='/cal/delete-snack/' class='delete-snack-form'>"
                f"    <input type='hidden' name='csrfmiddlewaretoken' value=''>"
                f"    <input type='hidden' name='snack_id' value='{snack.id}'>"
                f"    <input type='hidden' name='date' value='{self.year}-{self.month}-{day}'>"
                f"    <button type='submit' class='delete-button'><i class='fa-solid fa-x'></i></button>"
                f"</form></li>"
            )

        nutrition_table = (
            f"<table class='nutrition-table'>"
            f"<tr><th>Kcal</th><th>Protein</th><th>Fat</th><th>Carbs</th></tr>"
            f"<tr class='table-data'><td>{total_kcal:.1f}</td><td>{total_protein:.1f}g</td><td>{total_fat:.1f}g</td><td>{total_carbs:.1f}g</td></tr>"
            f"</table>"
        )

        highlight_class = "current-day" if datetime(self.year, self.month, day).date() == self.today else ""

        return (
            f"<td class='{highlight_class}'>"
            f"<div class='date-button-container'>"
            f"<span class='date'>{day}</span>"
            f"<button id='add-meal-btn' type='button' class='add-meal-btn' data-bs-toggle='modal' data-bs-target='#mealModal' data-date='{self.year}-{self.month}-{day}'>+</button>"
            f"</div>"
            f"<ul class='meal-list'>{meal_list}</ul>"
            f"{nutrition_table}"
            f"</td>"
        )

    def formatweek(self, theweek, meal_entries, snack_entries):
        return f"<tr>{''.join(self.formatday(d, meal_entries, snack_entries) for d, _ in theweek)}</tr>"

    def formatmonth(self, theyear, themonth, withyear=True):
        self.year = theyear
        self.month = themonth
        meal_entries = MealEntry.objects.filter(date__year=self.year, date__month=self.month, meal__creator=self.request.user)
        
        snack_entries = SnackEntry.objects.filter(date__year=self.year, date__month=self.month)

        cal = (
            f'<table border="0" cellspacing="2" class="calendar">\n'
            f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
            f'{self.formatweekheader()}\n<tbody>\n'
        )

        for week in self.monthdays2calendar(self.year, self.month):
            cal += self.formatweek(week, meal_entries, snack_entries) + "\n"

        cal += "</tbody>\n</table>\n"
        return cal

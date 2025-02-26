from datetime import datetime, timedelta
from calendar import HTMLCalendar, monthrange
from core.models import MealEntry

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        super().__init__()
        self.year = year
        self.month = month
        self.today = datetime.today().date()

    def formatday(self, day, meal_entry):
        if day == 0:  # Puste dni na początku/końcu miesiąca
            return "<td></td>"

        # Sprawdzenie, czy dzień istnieje w danym miesiącu
        days_in_month = monthrange(self.year, self.month)[1]
        if day > days_in_month:
            return "<td></td>"

        meal_entry_per_day = meal_entry.filter(date__day=day)

        # Sumowanie wartości odżywczych dla danego dnia
        total_kcal = total_protein = total_fat = total_carbs = 0
        meal_list = ""
        for meal in meal_entry_per_day:
            total_kcal += meal.meal.kcal * meal.portions
            total_protein += meal.meal.protein * meal.portions
            total_fat += meal.meal.fat * meal.portions
            total_carbs += meal.meal.carbs * meal.portions
            meal_list += f"<li>{meal} ({meal.portions}x) <button id='delete-button' data-date='{self.year}-{self.month}-{day}' meal-name='{meal.meal.recipe.name}' ><i class='fa-solid fa-x'></i></button></li>"
            # meal_list += f"<li>{meal.get_html_url} ({meal.portions}x) <button id='delete-button' data-date='{self.year}-{self.month}-{day}' meal-name='{meal.meal.recipe.name}' ><i class='fa-solid fa-x'></i></button></li>"

        # Generowanie tabeli wartości odżywczych (zmniejszona wersja)
        nutrition_table = (
            f"<table class='nutrition-table'>"
            f"<tr><th>Kcal</th><th>Protein</th><th>Fat</th><th>Carbs</th></tr>"
            f"<tr class='table-data'><td>{total_kcal:.1f}</td><td>{total_protein:.1f}g</td><td>{total_fat:.1f}g</td><td>{total_carbs:.1f}g</td></tr>"
            f"</table>"
        )

        # Sprawdzenie, czy to dzisiejsza data
        highlight_class = "current-day" if datetime(self.year, self.month, day).date() == self.today else ""

        return (
            f"<td class='{highlight_class}'>"
            f"<div class='date-button-container'>"
            f"<span class='date'>{day}</span>"
            f"<button id='add-meal-btn' type='button' class='add-meal-btn' data-bs-toggle='modal' data-bs-target='#mealModal' data-date='{self.year}-{self.month}-{day}'>+</button>"
            f"</div>"
            f"<ul class='meal-list'>{meal_list}</ul>"  # Dodanie listy posiłków
            f"{nutrition_table}"  # Dodanie tabeli z wartościami odżywczymi
            f"</td>"
        )

    def formatweek(self, theweek, meal_entry):
        return f"<tr>{''.join(self.formatday(d, meal_entry) for d, _ in theweek)}</tr>"

    def formatmonth(self, theyear, themonth, withyear=True):
        """Generuje tabelę HTML z kalendarzem na dany miesiąc."""
        self.year = theyear
        self.month = themonth
        meal_entry = MealEntry.objects.filter(date__year=self.year, date__month=self.month)

        cal = (
            f'<table border="0" cellpadding="2" cellspacing="2" class="calendar">\n'  # Zmniejszone paddingi
            f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
            f'{self.formatweekheader()}\n<tbody>\n'
        )

        for week in self.monthdays2calendar(self.year, self.month):
            cal += self.formatweek(week, meal_entry) + "\n"
        
        cal += "</tbody>\n</table>\n"
        return cal

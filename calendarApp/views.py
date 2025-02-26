
from datetime import datetime
import calendar
from django.http import JsonResponse

from django.views import generic
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta, date
from django.shortcuts import get_object_or_404
from django.utils.timezone import make_aware


from .forms import  MealForm
from .utils import Calendar

from core.models import Recipe, Product, Meal, MealEntry 



def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

class CalendarView(generic.ListView):
    model = MealEntry
    template_name = 'calendarApp/calendar.html'

    def get_context_data(self, **kwargs):
        d = get_date(self.request.GET.get('day', None))

        context = super().get_context_data(**kwargs)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)

        context["recipes"] = Recipe.objects.all()
        context["products"] = Product.objects.all()

        context["meals"] = Meal.objects.all()

        context["meal_core_form"] = MealForm()

        # use today's date for the calendar

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(d.year, d.month,withyear=True)
        context['calendar'] = mark_safe(html_cal)
        return context

    def post(self, request, *args, **kwargs):
            """Obsługa formularza dodawania posiłku."""
            message = None
            form = MealForm(request.POST)
            if form.is_valid():
                meal = form.cleaned_data.get("meal")
                portions = form.cleaned_data.get("portions")

                meal_obj = get_object_or_404(Meal, id=meal.id)
               
                if meal_obj.available_portions < portions:
                    message =f"You have only {meal_obj.available_portions} available portions of {meal_obj} meal"
                    return JsonResponse({"success": False,  "message": message})  

                meal_obj.available_portions -= portions
                meal_obj.save()

                if meal_obj.available_portions == 0:
                    message = f"This was a last portion of {meal_obj} "
                
                meal_entry = form.save()
                return JsonResponse({"success": True, "meal_id": meal_entry.id, "message": message})  # AJAX success

            return JsonResponse({"success": False, "errors": form.errors})  # AJAX error



def get_date(req_day):
    if req_day:
        try:
            year, month = map(int, req_day.split('-'))
            return make_aware(datetime(year, month, 1))  # Konwertujemy na datetime
        except ValueError:
            return make_aware(datetime.today())  # Domyślna wartość w przypadku błędu
    return make_aware(datetime.today())

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    return f"{prev_month.year}-{prev_month.month:02d}"  # Format YYYY-MM

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    return f"{next_month.year}-{next_month.month:02d}"  # Format YYYY-MM

        
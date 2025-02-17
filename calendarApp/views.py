
from datetime import datetime
import calendar
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta, date
from django.shortcuts import get_object_or_404
from django.utils.timezone import make_aware

from .models import Meal
from .forms import MealForm
from .utils import Calendar
from django.urls import reverse

class CalendarView(generic.ListView):
    model = Meal
    template_name = 'calendarApp/calendar.html'

    def get_context_data(self, **kwargs):
        d = get_date(self.request.GET.get('day', None))

        context = super().get_context_data(**kwargs)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)

        # use today's date for the calendar

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        return context

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




def event(request, meal_id=None):
    instance = Meal()
    if meal_id:
        instance = get_object_or_404(Meal, pk=meal_id)
    else:
        instance = Meal()
    
    form = MealForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('calendar'))
    return render(request, 'calendarApp/meal.html', {'form': form})
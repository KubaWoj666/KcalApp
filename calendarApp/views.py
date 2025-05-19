import calendar
from datetime import  datetime, timedelta

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.safestring import mark_safe
from django.utils.timezone import make_aware
from django.views import generic
from django.views.decorators.http import require_POST

from core.models import Meal, MealEntry, Product, SnackEntry
from .forms import MealForm, SnackEntryForm
from .utils import Calendar




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

        context["products"] = Product.objects.filter(creator=self.request.user)

        context["meal_core_form"] = MealForm(creator=self.request.user)
        context["snack_entry_form"] = SnackEntryForm(creator=self.request.user)

        # use today's date for the calendar

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month, self.request)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(d.year, d.month, withyear=True)
        context['calendar'] = mark_safe(html_cal)
        return context

    def post(self, request, *args, **kwargs):
            """Obsługa formularza dodawania posiłku."""
            user = request.user
            message = None
            form = MealForm(request.POST, creator=user)
            if form.is_valid():
                meal = form.cleaned_data.get("meal")
                portions = form.cleaned_data.get("portions")

                meal_obj = get_object_or_404(Meal, id=meal.id)

                if meal_obj.infinite_portions == True:
                    meal_entry = form.save()
                    return JsonResponse({"success": True, "meal_id": meal_entry.id, "message": message})  # AJAX success

               
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

@require_POST
def delete_meal_entry(request):
    meal_id = request.POST.get("meal_id")
    meal_entry_id = request.POST.get("meal_entry")
    
    meal_obj = get_object_or_404(Meal, id=meal_id)
    meal_entry_obj = get_object_or_404(MealEntry, id=meal_entry_id)

    if meal_obj.infinite_portions == True:
        meal_entry_obj.delete()
        return JsonResponse({"success": True})

    meal_obj.available_portions += meal_entry_obj.portions
    
    meal_obj.save()
    meal_entry_obj.delete()
    return JsonResponse({"success": True})

@require_POST
def add_snack_entry(request):
    user = request.user
    form = SnackEntryForm(request.POST or None, creator=user)

    if form.is_valid():    
        product = form.cleaned_data.get("product")
        grams = form.cleaned_data.get("grams")
        date = form.cleaned_data.get("date")
    
    product = get_object_or_404(Product, id=product.id)

    snack_obj = SnackEntry.objects.create(user=request.user, product=product, grams=grams, date=date)
    snack_obj.save()
    return redirect("calendar")

@require_POST
def delete_snack_entry(request):
    snack_id = request.POST.get("snack_id")
    snack_entry_obj = get_object_or_404(SnackEntry, id=snack_id)
    snack_entry_obj.delete()
    return JsonResponse({"success": True})
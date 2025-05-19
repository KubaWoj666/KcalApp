
from django.db.models import Sum, F
from core.models import MealEntry, SnackEntry

def calculate_snack_totals(snacks):
    """
    Calculates total nutrition values (kcal, protein, carbs, fat) from a SnackEntry queryset.
    Each snack's nutritional value is scaled by the gram amount (per 100g).
    
    Args:
        snacks (QuerySet): A queryset of SnackEntry objects.
    
    Returns:
        dict: A dictionary with total values for kcal, protein, carbs, and fat.
    """
    return {
        "kcal": sum((s.product.kcal * s.grams / 100 for s in snacks), 0),
        "protein": sum((s.product.protein * s.grams / 100 for s in snacks), 0),
        "carbs": sum((s.product.carbs * s.grams / 100 for s in snacks), 0),
        "fat": sum((s.product.fat * s.grams / 100 for s in snacks), 0),
    }


def aggregate_nutrition(user, date_from=None, date_to=None, today=None):
    """
    Aggregates total nutrition (kcal, protein, carbs, fat) from both MealEntry and SnackEntry models
    for a given user within a specified date range or for a single day.

    Args:
        user (UserAccount): The user whose data is being aggregated.
        date_from (date, optional): Start date (inclusive).
        date_to (date, optional): End date (exclusive).
        today (date, optional): If provided, aggregates only for that single day.
    
    Returns:
        dict: A dictionary with total values for kcal, protein, carbs, and fat.
    """
    if today:
        # Daily aggregation for a single day
        meal_data = MealEntry.objects.filter(meal__creator=user, date=today).aggregate(
            kcal=Sum(F("meal__kcal")),
            protein=Sum(F("meal__protein")),
            carbs=Sum(F("meal__carbs")),
            fat=Sum(F("meal__fat")),
        )
        snack_qs = SnackEntry.objects.filter(product__creator=user, date=today)
    else:
        # Aggregation over a date range
        meal_data = MealEntry.objects.filter(meal__creator=user, date__gte=date_from, date__lt=date_to).aggregate(
            kcal=Sum(F("meal__kcal")),
            protein=Sum(F("meal__protein")),
            carbs=Sum(F("meal__carbs")),
            fat=Sum(F("meal__fat")),
        )
        snack_qs = SnackEntry.objects.filter(product__creator=user, date__gte=date_from, date__lt=date_to)

    # Calculate snack totals and sum with meal totals
    snack_data = calculate_snack_totals(snack_qs)

    return {
        "kcal": round((meal_data.get("kcal") or 0) + snack_data.get("kcal", 0), 2),
        "protein": round((meal_data.get("protein") or 0) + snack_data.get("protein", 0), 2),
        "carbs": round((meal_data.get("carbs") or 0) + snack_data.get("carbs", 0), 2),
        "fat": round((meal_data.get("fat") or 0) + snack_data.get("fat", 0), 2),
    }


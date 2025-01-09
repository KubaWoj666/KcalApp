from django.shortcuts import render, redirect
from django.http import Http404

from .models import Product, Recipe, RecipeProduct
from .forms import ProductForm, RecipeProductForm

def home_view(request):
    recipes = Recipe.objects.all()
    context = {
        "recipes": recipes
    }
    return render(request, "core/home.html", context)


def add_and_fetch_product(request):
    form = ProductForm()
    
    try:
        products = Product.objects.all().order_by("name")
    except Exception as e:
        products = []
        print(f"Error fetching products {e}")

    if request.method == "POST":
        form = ProductForm(request.POST or None)
        action = request.POST.get("save")
        if action == "save":
            if form.is_valid():
                form.save()
            return redirect("home")
        if action == "save_add_another":
            if form.is_valid():
                form.save()
            return redirect("add_product")

    context = {
        "form": form,
        "products": products
    }

    return render(request, "core/add_product.html", context)


def recipe_detail(request, pk):
    try:
        recipe = Recipe.objects.get(id=pk)
        totals = recipe.calculate_total
        print(totals)
        
    except Recipe.DoesNotExist:
        raise Http404("Recipe not found")
    except Exception as e:
        recipe = None
        print(f"Error fetching products {e}")

    products = RecipeProduct.objects.filter(recipe=recipe)
    print(f"DUPA {products}" )


    
    context = {
        "recipe": recipe,
        "totals": totals,
        "products": products
    }

    return render(request, "core/recipe_detail.html", context)


def add_recipe(request):
    form = RecipeProductForm()

    context = {
        "form": form,
    }

    return render(request, "core/add_recipe.html", context)
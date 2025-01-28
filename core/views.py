from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404

from .models import Product, Recipe, RecipeProduct
from .forms import ProductForm, RecipeProductForm

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def home_view(request):
    recipes = Recipe.objects.all()
    request.session.pop("current_recipe_id", None)  

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
    
    context = {
        "recipe": recipe,
        "totals": totals,
        "products": products
    }

    return render(request, "core/recipe_detail.html", context)


def add_recipe(request):
    form = RecipeProductForm()
    data = {}

    try:
        products = Product.objects.all().order_by("name")
    except Exception as e:
        products = []
        print(f"Error fetching products {e}")

    if is_ajax:
        form = RecipeProductForm(request.POST or None)
        action = request.POST.get("action") 
        if form.is_valid(): 
            recipe_name = form.cleaned_data.get("name")
            recipe_id = request.session.get("current_recipe_id")
            if not recipe_id:
                
                recipe = Recipe.objects.create(name=recipe_name)
                request.session["current_recipe_id"] = recipe.id
            else:
                recipe = get_object_or_404(Recipe, id=recipe_id)
            
            if action == "add_products":
                print(action)
                product = form.cleaned_data.get("product")
                grams = form.cleaned_data.get("grams")
                RecipeProduct.objects.create(recipe=recipe, product=product, grams=grams)

                data["recipe_name"] = recipe_name
                data["product"] = product.name
                data["grams"] = grams
                

            return JsonResponse(data)
            
       
    context = {
        "form": form,
        "products": products
    }

    return render(request, "core/add_recipe.html", context)


def delete_from_product_list(request):

    if is_ajax:
        recipe_name = request.POST.get("recipe-name")
        product = request.POST.get("product")
        grams = request.POST.get("grams")

        recipe = get_object_or_404(Recipe, name=recipe_name)
        product = get_object_or_404(Product, name=product)
        product_to_delete = RecipeProduct.objects.get(recipe=recipe, product=product, grams=grams)
        product_to_delete.delete()

        return JsonResponse({"success": True})

    return JsonResponse({"success": False}, status=400)
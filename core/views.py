from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.http import Http404, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404

from .models import Product, Recipe, RecipeProduct, Meal
from .forms import ProductForm, RecipeProductForm, RecipeNameForm, RecipeGramsEditForm, AddProductToRecipeForm

from django_htmx.http import HttpResponseClientRefresh
from django.db.utils import IntegrityError
from decimal import Decimal

import json




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


#Recipe detail View
def recipe_detail(request, pk):
    add_product_form = AddProductToRecipeForm()
    product_form = ProductForm()
    form = RecipeNameForm()
    grams_edit_form = RecipeGramsEditForm()

    recipe = get_object_or_404(Recipe, id=pk)
    totals = recipe.calculate_total()  

    products = RecipeProduct.objects.filter(recipe=recipe)
    message = None

    #HTMX POST request for update product grams in recipe products
    if request.htmx:
        grams_edit_form = RecipeGramsEditForm(request.POST or None)
        if grams_edit_form.is_valid():
            product_name = request.POST.get("product-name")
            grams = grams_edit_form.cleaned_data.get("grams")
            product = products.filter(product__name=product_name).first()
            if product:
                product.grams = grams
                product.save()
                return HttpResponseClientRefresh()
            else:
                grams_edit_form.add_error("grams", "Product not found")       
        else:
            message = "wpisałeś ujemną bądź za duą liczbę"
        
    #POST request for update recipe name 
    if request.method == "POST":
        form = RecipeNameForm(request.POST or None, instance=recipe)
        if form.is_valid():
            form.save()
        return redirect("recipe_detail", pk=pk )  
    
    context = {
        "recipe": recipe,
        "totals": totals,
        "products": products,
        "form": form,
        "grams_edit_form": grams_edit_form,
        "message": message,
        "product_form": product_form,
        "add_product_form": add_product_form
    }

    return render(request, "core/recipe_detail.html", context)


@require_POST
def delete_recipe_product_from_recipe(request, pk):
    recipe = get_object_or_404(Recipe, id=pk)
    product_name = request.POST.get("delete-button")

    product_to_delete = RecipeProduct.objects.filter(recipe=recipe, product__name=product_name).first()

    if not product_to_delete:
        raise Http404("Product not found")
   
    product_to_delete.delete()
        
    return HttpResponseClientRefresh()


@require_POST
def add_product_to_recipe(request, pk):
    """Adding product to recipe"""
    recipe = get_object_or_404(Recipe, id=pk)
    form = AddProductToRecipeForm(request.POST or None)
    products = RecipeProduct.objects.filter(recipe=recipe)
    grams_edit_form = RecipeGramsEditForm()

    if request.method == "POST":
        if form.is_valid():
            product_obj = form.cleaned_data.get("product")
            grams = form.cleaned_data.get("grams")

            existing_product = RecipeProduct.objects.filter(recipe=recipe, product=product_obj).exists()
            if existing_product:
                # Error: product already on recipe
                return render(request, "core/recipe_detail.html", {
                    "recipe": recipe,
                    "products":products,
                    "grams_edit_form": grams_edit_form,
                    "add_product_form": form,
                    "error": "Product is already in Recipe"
                })

            try:
                RecipeProduct.objects.create(recipe=recipe, product=product_obj, grams=grams)
                return redirect("recipe_detail", pk=pk)  
            
            except IntegrityError:
                return render(request, "core/recipe_detail.html", {
                    "recipe": recipe,
                    "products": products,
                    "add_product_form": form,
                    "grams_edit_form": grams_edit_form,
                    "error": "Database error while adding product"
                })

    return redirect("recipe_detail", pk=pk)


def create_recipe(request):
    form = RecipeProductForm()
    add_product_form = ProductForm()
    data = {}

    try:
        products = Product.objects.all().order_by("name")
    except Exception as e:
        products = []

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
                product = form.cleaned_data.get("product")
                grams = form.cleaned_data.get("grams")
                RecipeProduct.objects.create(recipe=recipe, product=product, grams=grams)

                data["success"] = True
                data["recipe_name"] = recipe_name
                data["product"] = product.name
                data["grams"] = grams
            return JsonResponse(data)
                
    context = {
        "form": form,
        "products": products,
        "add_product_form": add_product_form,
    }

    return render(request, "core/add_recipe.html", context)

@require_POST
def delete_from_product_list(request):
    if is_ajax:
        recipe_name = request.POST.get("recipe-name")
        product = request.POST.get("product")
        grams = request.POST.get("grams")

        if not all([recipe_name, product, grams]):
            return JsonResponse({"success": False, "error": "Invalid Data"}, status=400)

        try:
            recipe = get_object_or_404(Recipe, name=recipe_name)
            product = get_object_or_404(Product, name=product)
            product_to_delete = RecipeProduct.objects.get(recipe=recipe, product=product, grams=grams)
            if not product_to_delete:
                return JsonResponse({"success": False, "error": "Product doesn't Exist "}, status=400)
            
            product_to_delete.delete()
            return JsonResponse({"success": True})
        except IntegrityError:
            return JsonResponse({"success": False, "error": "Błąd bazy danych"}, status=500)

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False}, status=400)


@require_POST
def create_product_from_add_recipe_template(request):
    
    if is_ajax:
        form = ProductForm(request.POST)
        if form.is_valid():
            new_product = form.save()
            return JsonResponse({"success": True, 
                                 "new_product": {
                                     "id": new_product.id,
                                     "name": new_product.name,
                                     "kcal": new_product.kcal
                                 }})
        return JsonResponse({"success": False, "errors": form.errors}, status=400)

    return JsonResponse({"error": "Metoda niedozwolona"}, status=405)


def plan_meal_view(request):
    recipes = Recipe.objects.all()
    products = Product.objects.all()


    context = {
        "recipes": recipes,
        "products": products
    }

    return render(request, "core/plan_meal.html", context)


def get_recipe(request, pk):
    recipe = get_object_or_404(Recipe, id=pk)
    
    ingredients = RecipeProduct.objects.filter(recipe=recipe).select_related("product")

    totals = recipe.calculate_total()

    data = {
        "name": recipe.name,
        "ingredients": [
            {
                "product": item.product.name,
                "grams": item.grams,
                "kcal": item.product.kcal,
                "protein": item.product.protein,
                "fat": item.product.fat,
                "carbs": item.product.carbs,
            }
            for item in ingredients
        ],
        "totals": totals
    }

    return JsonResponse(data)


def get_product(request, pk):
    product = get_object_or_404(Product, id=pk)

    data = {
        "product": product
    }

    return JsonResponse(data)


@require_POST
def create_meal(request):
    """
    Handles meal creation by associating it with a selected recipe.
    Extracts nutritional data and portion quantity from the request.
    """
    try:
        
        recipe_id = request.POST.get("recipe_id")
        nutrition = request.POST.getlist("nutrition[]")
        num_of_portions = request.POST.get("num_of_portions")

      
        if not (recipe_id and nutrition and num_of_portions):
            return JsonResponse({"success": False, "error": "Missing required fields"})

        recipe = get_object_or_404(Recipe, id=recipe_id)

        try:
            kcal, protein, fat, carbs = map(Decimal, nutrition)
            num_of_portions = int(num_of_portions)
        except (InvalidOperation, ValueError):
            return JsonResponse({"success": False, "error": "Invalid numerical values"})

        meal = Meal.objects.create(
            recipe=recipe,
            kcal=kcal,
            protein=protein,
            fat=fat,
            carbs=carbs,
            total_portions=num_of_portions,
            available_portions=num_of_portions
        )

        meal.save()

        return JsonResponse({"success": True, "message": "Meal created successfully"})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)

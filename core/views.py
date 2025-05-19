from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.db.utils import IntegrityError
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django_htmx.http import HttpResponseClientRefresh

from .models import Product, Recipe, RecipeProduct, Meal, MealEntry
from .forms import (
    ProductForm,
    RecipeProductForm,
    RecipeNameForm,
    RecipeGramsEditForm,
    AddProductToRecipeForm
)

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def home_view(request):
    user = request.user
    recipes = Recipe.objects.all()
    request.session.pop("current_recipe_id", None)  

    context = {
        "recipes": recipes,
        "user": user

    }
    return render(request, "core/home.html", context)


def add_and_fetch_product(request):
    user = request.user
    form = ProductForm(creator=user) if request.method != "POST" else ProductForm(request.POST, creator=user)

    products = Product.objects.filter(creator=user).order_by("name")

    if request.method == "POST":
        action = request.POST.get("save")

        if form.is_valid():
            try:
                form.save()
                if action == "save":
                    return redirect("home")
                elif action == "save_add_another":
                    return redirect("add_product")
            except IntegrityError:
                messages.error(request, "Product already exists!")
        else:
            messages.error(request, "Form contains errors.")

    context = {
        "form": form,
        "products": products,
    }

    return render(request, "core/add_product.html", context)


def product_detail(request, pk):
    user = request.user
    product = Product.objects.get(id=pk, creator=user)
    form = ProductForm(instance=product)

    if request.method == "POST":
        form = ProductForm(request.POST or None, instance=product)
        if form.is_valid():
            form.save()

    context = {
        "product": product,
        "form": form,
        
    }

    return render(request, "core/product_detail.html", context)


#Recipe detail View
def recipe_detail(request, pk):
    """
    Displays and handles interactions with a specific recipe, including:
    - Updating recipe name
    - Editing ingredient amounts (grams)
    - Showing calculated totals and existing ingredients
    """
    user = request.user
    add_product_form = AddProductToRecipeForm(creator=user)
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
            message = "Invalid value"
        
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
    user = request.user
    recipe = get_object_or_404(Recipe, id=pk)
    form = AddProductToRecipeForm(creator=user)
    products = RecipeProduct.objects.filter(recipe=recipe)
    grams_edit_form = RecipeGramsEditForm()

    if request.method == "POST":
        form = AddProductToRecipeForm(request.POST or None, creator=user)
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
    user = request.user
    form = RecipeProductForm()
    add_product_form = ProductForm()
    user = request.user
    data = {}


    try:
        products = Product.objects.filter(creator=user).order_by("name")
    except Exception as e:
        products = []

    if is_ajax:
        form = RecipeProductForm(request.POST or None, creator=user)
        action = request.POST.get("action") 
        if form.is_valid(): 
            recipe_name = form.cleaned_data.get("name")
            recipe_id = request.session.get("current_recipe_id")

            if not recipe_id:           
                recipe = Recipe.objects.create(name=recipe_name, creator=user)
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
    user = request.user

    if is_ajax:
        form = ProductForm(request.POST, creator=user)

        if form.is_valid():
            try:
                new_product = form.save()
                return JsonResponse({
                    "success": True,
                    "new_product": {
                        "id": new_product.id,
                        "name": new_product.name,
                        "kcal": new_product.kcal,
                    }
                })
            except IntegrityError:
                
                return JsonResponse({
                    "success": False,
                    "message": "Product already exist!"
                })   
        else:
            return JsonResponse({
                "success": False,
                "message": "Formularz zawiera błędy.",
                "errors": form.errors
            })  # status=200

    return JsonResponse({"error": "Nieprawidłowe żądanie."}, status=400)

def plan_meal_view(request):
    user = request.user
    recipes = Recipe.objects.filter(creator=user)
    products = Product.objects.filter(creator=user).order_by("name")


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
    user = request.user
    try:
        
        recipe_id = request.POST.get("recipe_id")
        nutrition = request.POST.getlist("nutrition[]")
        num_of_portions = request.POST.get("num_of_portions")
        infinite_portions = request.POST.get("infinite_portions")
      
        if not (recipe_id and nutrition and num_of_portions and infinite_portions):
            return JsonResponse({"success": False, "error": "Missing required fields"})

        recipe = get_object_or_404(Recipe, id=recipe_id)

        try:
            kcal, protein, fat, carbs = map(Decimal, nutrition)
            num_of_portions = int(num_of_portions)
        except (InvalidOperation, ValueError):
            return JsonResponse({"success": False, "error": "Invalid numerical values"})

        if infinite_portions == "true":
            meal = Meal.objects.create(
                creator=user,
                recipe=recipe,
                kcal=kcal,
                protein=protein,
                fat=fat,
                carbs=carbs,
                total_portions=None,
                available_portions=None,
                infinite_portions=True
            )
        
        else:
            meal = Meal.objects.create(
                creator=user,
                recipe=recipe,
                kcal=kcal,
                protein=protein,
                fat=fat,
                carbs=carbs,
                total_portions=num_of_portions,
                available_portions=num_of_portions,
                infinite_portions=False
            )

        meal.save()

        return JsonResponse({"success": True, "message": "Meal created successfully"})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


def meal_entry_detail(request, pk):
    meal_entry = get_object_or_404(MealEntry, id=pk)

    if hasattr(meal_entry.meal, 'recipe'):
        products = meal_entry.meal.recipe.products.all()
    else:
        products = []  

    recipe = meal_entry.meal.recipe
    product_recipe = RecipeProduct.objects.filter(recipe=recipe)

    context = {
        "meal_entry": meal_entry,
        "products": products,
        "product_recipe": product_recipe
    }

    return render(request, "core/meal_entry_detail.html", context)
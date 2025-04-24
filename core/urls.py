from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("recipe-detail/<int:pk>/", views.recipe_detail, name="recipe_detail"),
    path("delete-product-from-recipe/<int:pk>/", views.delete_recipe_product_from_recipe, name="delete_recipe_product"),
    path("add-product-to-recipe/<int:pk>/", views.add_product_to_recipe, name="add_product_to_recipe"),
    path("add-product/", views.add_and_fetch_product, name="add_product"),
    path("product-detail/<int:pk>", views.product_detail, name="product_detail"),
    path("add-recipe/", views.create_recipe, name="add_recipe"),
    path("delete-from-product-list/", views.delete_from_product_list, name="delete_from_product_list"),
    path("create-product/", views.create_product_from_add_recipe_template, name="create_product"),
    path("plan-meal/", views.plan_meal_view, name="plan_meal"),
    path("get-recipe/<int:pk>/", views.get_recipe, name="get-recipe"),
    path("save-meal/", views.create_meal, name="save-meal"),
    path("meal-entry-detail/<int:pk>/", views.meal_entry_detail, name="meal_entry_detail")
]
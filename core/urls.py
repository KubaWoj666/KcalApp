from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("recipe-detail/<int:pk>/", views.recipe_detail, name="recipe_detail"),
    path("delete-product-from-recipe/<int:pk>/", views.delete_recipe_product_from_recipe, name="delete_recipe_product"),
    path("add-product-to-recipe/<int:pk>/", views.add_product_to_recipe, name="add_product_to_recipe"),
    path("add-product/", views.add_and_fetch_product, name="add_product"),
    path("add-recipe/", views.add_recipe, name="add_recipe"),
    path("delete-from-product-list/", views.delete_from_product_list, name="delete_from_product_list"),
    path("create-product/", views.create_product_from_add_recipe_template, name="create_product"),
]
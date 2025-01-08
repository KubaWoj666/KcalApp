from django.shortcuts import render, redirect

from .models import Product
from .forms import ProductForm

def home_view(request):
    return render(request, "core/home.html")


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
        "form":form,
        "products":products
    }

    return render(request, "core/add_product.html", context)


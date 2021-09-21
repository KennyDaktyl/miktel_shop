from django.views import View
from django.shortcuts import render, redirect

from web.models import Products, Category, products


class ProductsCategory(View):
    def get(self, request ,slug):
        cat = Category.objects.get(slug=slug)
        products = Products.objects.filter(category=cat).filter(is_active=True)
        ctx = {'cat': cat, 'products': products}
        return render(request, "products/products_list.html", ctx)

products_category = ProductsCategory.as_view()
from django.views import View
from django.shortcuts import render, redirect

from web.models import Products, Category, SubCategory


class SubCategoryItems(View):
    def get(self, request ,cat, sub_cat):
        sub_cat = SubCategory.objects.get(slug=sub_cat)
        products = Products.objects.filter(sub_category=sub_cat).filter(is_active=True)
        ctx = {'sub_cat': sub_cat, 'products': products}
        return render(request, "products/products_list.html", ctx)


class ProductDetails(View):
    def get(self, request ,cat, sub_cat, product):
        product = Products.objects.get(slug=product)
        ctx = {'product': product}
        return render(request, "products/product_details.html", ctx)

sub_category_items = SubCategoryItems.as_view()
product_details = ProductDetails.as_view()
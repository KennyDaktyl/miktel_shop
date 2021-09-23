from django.views import View
from django.shortcuts import render, redirect

from web.models import Products, Category, SubCategory, SubCategoryType

class ShopMainView(View):
    def get(self, request):
        cat = Category.objects.all()
        products = Products.objects.filter(is_news=True).filter(is_active=True)
        ctx = {'cat': cat, 'products': products}
        return render(request, "products/products_list.html", ctx)

class SubCategoryProducts(View):
    def get(self, request ,cat, sub_cat):
        sub_cat = SubCategory.objects.get(slug=sub_cat)
        products = Products.objects.filter(sub_category_type__sub_category=sub_cat).filter(is_active=True)
        ctx = {'sub_cat': sub_cat, 'products': products}
        return render(request, "products/products_list.html", ctx)

class SubCategoryTypeProducts(View):
    def get(self, request ,cat, sub_cat, sub_cat_type):
        sub_category_type = SubCategoryType.objects.get(slug=sub_cat_type)
        products = Products.objects.filter(sub_category_type=sub_category_type).filter(is_active=True)
        ctx = {'sub_category_type': sub_category_type, 'products': products}
        return render(request, "products/products_list.html", ctx)

class ProductDetails(View):
    def get(self, request, cat, sub_cat, sub_cat_type, product):
        product = Products.objects.get(slug=product)
        ctx = {'sub_category_type': product.sub_category_type, 'product': product}
        return render(request, "products/product_details.html", ctx)




sub_category_products = SubCategoryProducts.as_view()
sub_category_type = SubCategoryTypeProducts.as_view()
product_details = ProductDetails.as_view()
shop_main_view = ShopMainView.as_view()
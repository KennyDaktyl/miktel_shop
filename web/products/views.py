from django.db.models import Q

from django.views import View
from django.shortcuts import render, redirect
from rest_framework import viewsets, generics

from web.models import Products, Category, SubCategory, SubCategoryType
from .serializers import ProductSerializer

from functools import reduce
from operator import and_, or_


class ShopMainView(View):
    def get(self, request):
        cat = Category.objects.all()
        products = Products.objects.filter(is_news=True).filter(is_active=True)
        title = "Serwis w Rybnej | Sklep on-line"
        description = "W sklepie znajdą Państwo telefony komórkowe oraz akcesoria GSM. Pieczątki firmowe, imienne oraz datowniki. W ofercie również grawerowane tabliczki i gadżety. "
        ctx = {'cat': cat, 'products': products,
               'title': title, 'description': description}
        return render(request, "products/products_list.html", ctx)


class SubCategoryProducts(View):
    def get(self, request, cat, sub_cat):
        sub_cat = SubCategory.objects.get(slug=sub_cat)
        products = Products.objects.filter(
            sub_category_type__sub_category=sub_cat).filter(is_active=True)
        title = ""
        description = ""
        ctx = {'sub_cat': sub_cat, 'products': products,
               'title': title, 'description': description}
        return render(request, "products/products_list.html", ctx)


class SubCategoryTypeProducts(View):
    def get(self, request, cat, sub_cat, sub_cat_type):
        sub_category_type = SubCategoryType.objects.get(slug=sub_cat_type)
        products = Products.objects.filter(
            sub_category_type=sub_category_type).filter(is_active=True)
        title = sub_category_type.sub_category.name + " | " + sub_category_type.name
        description = "Produkty z kategorii: " + \
            sub_category_type.sub_category.name + " | " + sub_category_type.name
        ctx = {'sub_category_type': sub_category_type,
               'products': products, 'title': title, 'description': description}
        return render(request, "products/products_list.html", ctx)


class ProductDetails(View):
    def get(self, request, cat, sub_cat, sub_cat_type, product):
        product = Products.objects.get(slug=product)
        ctx = {'sub_category_type': product.sub_category_type, 'product': product}
        return render(request, "products/product_details.html", ctx)


class ApiProductsListSet(generics.ListAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        search = self.request.query_params.get('search')
        products = Products.objects.all()
        q_object = reduce(and_, (Q(sub_category_type__sub_category__category__name__contains=search)
                                 | Q(sub_category_type__sub_category__name__contains=search)
                                 | Q(sub_category_type__name__contains=search)
                                 | Q(brand__name__contains=search)
                                 | Q(name__contains=search)
                                 for search in search))
        products = products.filter(q_object)
        print((products).count())
        # products = Products.objects.filter(name__icontains=search)
        return products[0:20]


shop_main_view = ShopMainView.as_view()
sub_category_products = SubCategoryProducts.as_view()
sub_category_type = SubCategoryTypeProducts.as_view()
product_details = ProductDetails.as_view()
search_products = ApiProductsListSet.as_view()

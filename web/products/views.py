import imp
from django.contrib import messages
from django.db.models import Q

from django.views import View
from django.shortcuts import render, redirect
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from django.http import HttpResponse


from web.models import Products, Category, SubCategory, SubCategoryType
from web.models.products import Images
from .serializers import ProductSerializer

from functools import reduce
from operator import and_, or_

from .forms import *


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
    def get(self, request, cat, sub_cat, pk):
        sub_cat = SubCategory.objects.get(pk=pk)
        products = Products.objects.filter(
            sub_category_type__sub_category=sub_cat).filter(is_active=True)
        title = ""
        description = ""
        ctx = {'sub_cat': sub_cat, 'products': products,
               'title': title, 'description': description}
        return render(request, "products/sub_category_details.html", ctx)


class SubCategoryTypeProducts(View):
    def get(self, request, cat, sub_cat, sub_cat_type, pk):
        sub_category_type = SubCategoryType.objects.get(pk=pk)
        products = Products.objects.filter(
            sub_category_type=sub_category_type).filter(is_active=True)
        title = sub_category_type.sub_category.name + " | " + sub_category_type.name
        description = "Produkty z kategorii: " + \
            sub_category_type.sub_category.name + " | " + sub_category_type.name
        ctx = {'sub_category_type': sub_category_type,
               'products': products, 'title': title, 'description': description}
        return render(request, "products/products_list.html", ctx)


class ProductDetails(View):
    def get(self, request, cat, sub_cat, sub_cat_type, product, pk):
        product = Products.objects.get(pk=pk)
        if request.user.is_staff:
            photo_m_form = MainPhotoProductForm()
            details_form = SelectDetailsProductForm(instance=product)
            ctx = {'sub_category_type': product.sub_category_type,
                   'product': product, 'photo_m_form': photo_m_form, "details_form": details_form}
            return render(request, "products/product_details.html", ctx)

        ctx = {'sub_category_type': product.sub_category_type, 'product': product}
        return render(request, "products/product_details.html", ctx)

    def post(self, request, cat, sub_cat, sub_cat_type, product, pk):
        product = Products.objects.get(pk=pk)
        photo_m_form = MainPhotoProductForm(
            request.POST, request.FILES)
        details_form = SelectDetailsProductForm(request.POST, instance=product)
        if request.POST.get('photo_main'):
            if photo_m_form.is_valid():
                product.image = request.FILES.get('image')
                product.alt = photo_m_form.cleaned_data["alt"]
                product.title = photo_m_form.cleaned_data["title"]
                product.save()
                messages.error(request, 'Zaktualizowno szczegóły produktu.')
                return redirect('product_details', cat=product.sub_category_type.sub_category.category.slug, sub_cat=product.sub_category_type.sub_category.slug, sub_cat_type=product.sub_category_type.slug, product=product.slug, pk=product.id)
            else:
                messages.error(request, 'Błąd formularza')
                photo_m_form = MainPhotoProductForm(
                    request.POST, request.FILES)
                details_form = SelectDetailsProductForm(instance=product)
                ctx = {'sub_category_type': product.sub_category_type,
                       'product': product, 'photo_m_form': photo_m_form, "details_form": details_form}
                return render(request, "products/product_details.html", ctx)

        if request.POST.get('photo_gallery'):
            if photo_m_form.is_valid():
                image = Images()
                image.image = request.FILES.get('image')
                image.alt = photo_m_form.cleaned_data["alt"]
                image.title = photo_m_form.cleaned_data["title"]
                image.product = product
                image.save()
                messages.error(request, 'Zaktualizowno szczegóły produktu.')
                return redirect('product_details', cat=product.sub_category_type.sub_category.category.slug, sub_cat=product.sub_category_type.sub_category.slug, sub_cat_type=product.sub_category_type.slug, product=product.slug, pk=product.id)
            else:
                messages.error(request, 'Błąd formularza')
                photo_m_form = MainPhotoProductForm(
                    request.POST, request.FILES)
                details_form = SelectDetailsProductForm(instance=product)
                ctx = {'sub_category_type': product.sub_category_type,
                       'product': product, 'photo_m_form': photo_m_form, "details_form": details_form}
                return render(request, "products/product_details.html", ctx)

        if request.POST.get('add_details'):
            if details_form.is_valid():
                details_form.save()
                messages.error(request, 'Zaktualizowno szczegóły produktu.')
                return redirect('product_details', cat=product.sub_category_type.sub_category.category.slug, sub_cat=product.sub_category_type.sub_category.slug, sub_cat_type=product.sub_category_type.slug, product=product.slug, pk=product.id)
            else:
                messages.error(request, 'Błąd formularza')
                photo_m_form = MainPhotoProductForm()
                details_form = SelectDetailsProductForm(
                    request.POST, instance=product)
                ctx = {'sub_category_type': product.sub_category_type,
                       'product': product, 'photo_m_form': photo_m_form, "details_form": details_form}
                return render(request, "products/product_details.html", ctx)

        

class ApiProductsListSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    template_name = "products/products_list.html"
    renderer_classes = [TemplateHTMLRenderer]

    def get_queryset(self):
        search = self.request.query_params.get('search')
        products = Products.objects.all()
        # q_object = reduce(and_, (Q(sub_category_type__sub_category__category__name__contains=search)
        #                          | Q(sub_category_type__sub_category__name__contains=search)
        #                          | Q(sub_category_type__name__contains=search)
        #                          | Q(brand__name__contains=search)
        #                          | Q(name__contains=search)
        #                          for search in search))
        # products = products.filter(q_object)
        # for prod in products:
        #     print(prod)
        products = Products.objects.filter(name__icontains=search)
        return products[0:20]

    def post(self, request, *args, **kwargs):
        search = request.POST["search"]
        products = Products.objects.filter(name__icontains=search)
        # products = Products.objects.all()
        # serializer = ProductSerializer(products, many=True)
        serializer = self.get_serializer(products, many=True)
        ctx = {'products': serializer.data}
        return render(request, self.template_name, ctx)
        return HttpResponse(serializer.data)

class ApiProductsListSetJS(generics.ListAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        search = self.request.query_params.get('search')
        products = Products.objects.all()
        # q_object = reduce(and_, (Q(sub_category_type__sub_category__category__name__contains=search)
        #                          | Q(sub_category_type__sub_category__name__contains=search)
        #                          | Q(sub_category_type__name__contains=search)
        #                          | Q(brand__name__contains=search)
        #                          | Q(name__contains=search)
        #                          for search in search))
        # products = products.filter(q_object)
        # for prod in products:
        #     print(prod)
        products = Products.objects.filter(name__icontains=search)
        return products[0:20]

shop_main_view = ShopMainView.as_view()
sub_category_products = SubCategoryProducts.as_view()
sub_category_type = SubCategoryTypeProducts.as_view()
product_details = ProductDetails.as_view()
search_products = ApiProductsListSet.as_view({'get': 'post'})
search_products_js = ApiProductsListSetJS.as_view()

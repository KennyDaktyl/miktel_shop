import os
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import ListView
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from numpy import size
from rest_framework import generics, viewsets
from rest_framework.renderers import TemplateHTMLRenderer
from web.models import Category, Products, SubCategory, SubCategoryType, Size

from .forms import AddGalleryPhotoForm, AddMainPhotoForm, SelectDetailsProductForm
from .serializers import ProductSerializer


class ShopMainView(View):
    def get(self, request):
        cat = Category.objects.all()
        products = Products.objects.filter(is_news=True).filter(is_active=True)
        title = "Serwis w Rybnej | Sklep on-line"
        description = "W sklepie znajdą Państwo telefony komórkowe oraz \
            akcesoria GSM. Pieczątki firmowe, imienne oraz datowniki. \
                W ofercie również grawerowane tabliczki i gadżety. "
        ctx = {
            "cat": cat,
            "products": products,
            "title": title,
            "description": description,
        }
        return render(request, "products/products_list.html", ctx)


class SubCategoryProducts(ListView):
    template_name = "products/sub_category_details.html"
    paginate_by = 20
    model = Products

    def get_queryset(self):
        self.sub_cat = get_object_or_404(SubCategory, pk=self.kwargs["pk"])
        return Products.objects.filter(
            sub_category_type__sub_category=self.sub_cat
        ).filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sub_category"] = self.sub_cat
        return context


class SubCategoryTypeProducts(ListView):
    template_name = "products/products_list.html"
    paginate_by = 20
    model = Products

    def get_queryset(self):
        self.sub_category_type = get_object_or_404(
            SubCategoryType, pk=self.kwargs["pk"]
        )
        return Products.objects.filter(sub_category_type=self.sub_category_type).filter(
            is_active=True
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sub_category_type"] = self.sub_category_type
        sizes_pk = self.object_list.values_list(
            'size', flat=True).distinct().order_by()
        context["sizes"] = Size.objects.filter(pk__in=[sizes_pk])
        return context


class ProductDetails(DetailView):
    template_name = "products/product_details.html"
    model = Products
    success_message_add = "Zaktualizowno szczegóły produktu."
    success_message_error = "Błąd formularza"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_staff:
            context["photo_m_form"] = AddMainPhotoForm(instance=self.object)
            context["photo_g_form"] = AddGalleryPhotoForm(
                initial={"product": self.object})
            context["details_form"] = SelectDetailsProductForm(
                instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        photo_m_form = AddMainPhotoForm(
            request.POST, request.FILES, instance=self.object
        )
        photo_g_form = AddGalleryPhotoForm(
            request.POST, request.FILES, initial={"product": self.object}
        )
        details_form = SelectDetailsProductForm(
            request.POST, instance=self.object)
        context = super(ProductDetails, self).get_context_data(**kwargs)
        if request.POST.get("photo_main"):
            if photo_m_form.is_valid():
                photo_m_form.save()
                context["photo_m_form"] = photo_m_form
                context["photo_g_form"] = AddGalleryPhotoForm(
                    initial={"product": self.object})
                context["details_form"] = SelectDetailsProductForm(
                    instance=self.object)
                messages.success(self.request, self.success_message_add)
                return self.render_to_response(context=context)
            else:
                context["photo_m_form"] = photo_m_form
                context["photo_g_form"] = AddGalleryPhotoForm(
                    initial={"product": self.object})
                context["details_form"] = SelectDetailsProductForm(
                    instance=self.object)
                messages.success(self.request, self.success_message_error)
                return self.render_to_response(context=context)
        if request.POST.get("photo_gallery"):
            if photo_g_form.is_valid():
                photo_g_form.save()
                context["photo_m_form"] = AddMainPhotoForm(
                    instance=self.object)
                context["photo_g_form"] = AddGalleryPhotoForm(
                    initial={"product": self.object})
                context["details_form"] = SelectDetailsProductForm(
                    instance=self.object)
                messages.success(self.request, self.success_message_add)
                return self.render_to_response(context=context)
            else:
                context["photo_m_form"] = AddMainPhotoForm(
                    instance=self.object)
                context["photo_g_form"] = photo_g_form
                context["details_form"] = SelectDetailsProductForm(
                    instance=self.object)
                messages.success(self.request, self.success_message_error)
                return self.render_to_response(context=context)
        if request.POST.get("add_details"):
            if details_form.is_valid():
                details_form.save()
                context["photo_m_form"] = AddMainPhotoForm(
                    instance=self.object)
                context["photo_g_form"] = AddGalleryPhotoForm(
                    initial={"product": self.object})
                context["details_form"] = details_form
                messages.success(self.request, self.success_message_add)
                return self.render_to_response(context=context)
            else:
                context["photo_m_form"] = AddMainPhotoForm(
                    instance=self.object)
                context["photo_g_form"] = AddGalleryPhotoForm(
                    initial={"product": self.object})
                context["details_form"] = details_form
                messages.success(self.request, self.success_message_error)
                return self.render_to_response(context=context)


class ProductRedirectView(RedirectView):
    permanent = True
    query_string = True
    pattern_name = "product_details"

    def get(self, *args, **kwargs):
        product = get_object_or_404(Products, pk=kwargs["pk"])
        return redirect(product.get_absolute_url(), status=301)


class SubCategoryRedirectView(RedirectView):
    permanent = True
    query_string = True

    def get(self, *args, **kwargs):
        sub_category = get_object_or_404(
            SubCategory, slug=kwargs["sub_cat"], pk=kwargs["pk"])
        print(sub_category.get_absolute_url())
        return redirect(sub_category.get_absolute_url(), status=301)


class SubCategoryTypeRedirectView(RedirectView):
    permanent = True
    query_string = True

    def get(self, *args, **kwargs):
        sub_category_type = get_object_or_404(
            SubCategoryType, slug=kwargs["sub_cat_type"], pk=kwargs["pk"])
        return redirect(sub_category_type.get_absolute_url(), status=301)


class ApiProductsListSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    template_name = "products/products_list.html"
    renderer_classes = [TemplateHTMLRenderer]

    def get_queryset(self):
        search = self.request.query_params.get("search")
        products = Products.objects.filter(name__icontains=search)
        return products[0:20]

    def post(self, request, *args, **kwargs):
        search = request.POST["search"]
        products = Products.objects.filter(name__icontains=search)
        ctx = {"object_list": products}
        return render(request, self.template_name, ctx)


class ApiProductsListSetJS(generics.ListAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        search = self.request.query_params.get("search")
        products = Products.objects.filter(name__icontains=search)
        return products[0:20]


shop_main_view = ShopMainView.as_view()
sub_category_products = SubCategoryProducts.as_view()
sub_category_type = SubCategoryTypeProducts.as_view()
product_details = ProductDetails.as_view()
redirect_product = ProductRedirectView.as_view()
redirect_sub_category = SubCategoryRedirectView.as_view()
redirect_sub_category_type = SubCategoryTypeRedirectView.as_view()
search_products = ApiProductsListSet.as_view({"get": "post"})
search_products_js = ApiProductsListSetJS.as_view()

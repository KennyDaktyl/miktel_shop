from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from rest_framework import generics, viewsets
from rest_framework.renderers import TemplateHTMLRenderer

from web.models import Category, Products, SubCategory, SubCategoryType

from .forms import AddMainPhotoForm, SelectDetailsProductForm
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
        context["sub_cat"] = self.sub_cat
        return context


class SubCategoryTypeProducts(ListView):
    template_name = "products/products_list.html"
    paginate_by = 20
    model = Products

    def get_queryset(self):
        self.sub_category_type = get_object_or_404(
            SubCategoryType, pk=self.kwargs["pk"]
        )
        return Products.objects.filter(
            sub_category_type=self.sub_category_type
        ).filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sub_category_type"] = self.sub_category_type
        context["title"] = (
            self.sub_category_type.sub_category.name
            + " | "
            + self.sub_category_type.name
        )
        context["description"] = self.sub_category_type
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
            context["details_form"] = SelectDetailsProductForm(
                instance=self.object
            )
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        photo_m_form = AddMainPhotoForm(
            request.POST, request.FILES, instance=self.object
        )
        details_form = SelectDetailsProductForm(
            request.POST, instance=self.object
        )
        context = super(ProductDetails, self).get_context_data(**kwargs)
        if request.POST.get("photo_main"):
            if photo_m_form.is_valid():
                photo_m_form.save()
                context["photo_m_form"] = photo_m_form
                context["details_form"] = SelectDetailsProductForm(
                    instance=self.object
                )
                messages.success(self.request, self.success_message_add)
                return self.render_to_response(context=context)
            else:
                context["photo_m_form"] = photo_m_form
                context["details_form"] = SelectDetailsProductForm(
                    instance=self.object
                )
                messages.success(self.request, self.success_message_error)
                return self.render_to_response(context=context)
        if request.POST.get("add_details"):
            if details_form.is_valid():
                details_form.save()
                context["photo_m_form"] = AddMainPhotoForm(
                    instance=self.object)
                context["details_form"] = details_form
                messages.success(self.request, self.success_message_add)
                return self.render_to_response(context=context)
            else:
                context["photo_m_form"] = AddMainPhotoForm(
                    instance=self.object)
                context["details_form"] = details_form
                messages.success(self.request, self.success_message_error)
                return self.render_to_response(context=context)


class ApiProductsListSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    template_name = "products/products_list.html"
    renderer_classes = [TemplateHTMLRenderer]

    def get_queryset(self):
        search = self.request.query_params.get("search")
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
        ctx = {"products": serializer.data}
        return render(request, self.template_name, ctx)
        return HttpResponse(serializer.data)


class ApiProductsListSetJS(generics.ListAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        search = self.request.query_params.get("search")
        # search_tab = search.split(" ")
        # products = Products.objects.all()

        # q_object = reduce(
        #         or_, (Q(name__contains=search) for search in search_tab))
        # products = products.filter(q_object)
        # products = Products.objects.filter(
        #     Q(name__icontains=search) for search in search_tab)
        # print(search)
        # print(search_tab)
        # q_object = reduce(and_, (Q(sub_category_type__name__contains=search) for search in search_tab))
        # products = products.filter(q_object)
        # q_object = reduce(
        #     and_, (Q(name__contains=search) for search in search_tab))
        # products = products.filter(q_object)
        # print(products)
        # for prod in products:
        #     print(prod)
        products = Products.objects.filter(name__icontains=search)
        return products[0:20]


shop_main_view = ShopMainView.as_view()
sub_category_products = SubCategoryProducts.as_view()
sub_category_type = SubCategoryTypeProducts.as_view()
product_details = ProductDetails.as_view()
search_products = ApiProductsListSet.as_view({"get": "post"})
search_products_js = ApiProductsListSetJS.as_view()

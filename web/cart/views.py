import json
from nis import cat

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from web.constans import DELIVERY_TYPE
from web.models import Category, PayMethod, Products
from .cart import Cart


class AddProductView(View):
    def post(self, request):
        if request.is_ajax():
            prod_id = request.POST.get("prod_id")
            product = Products.objects.get(pk=int(prod_id))
            qty = request.POST.get("qty")
            cart = Cart(request)
            cart.add(product=product, quantity=qty)
            dict_obj = {
                "total": float(cart.get_total_price()),
                "len": cart.len(),
                "in_stock": product.qty - int(qty),
            }
            serialized = json.dumps(dict_obj)
            return HttpResponse(serialized)


class EditQtyProduct(View):
    def post(self, request):
        if request.is_ajax():
            prod_id = request.POST.get("prod_id")
            product = Products.objects.get(pk=int(prod_id))
            qty = int(request.POST.get("qty"))

            cart = Cart(request)
            cart.add(product=product, quantity=qty, update_quantity=True)
            cart_dict = request.session.get(settings.CART_SESSION_ID)
            dict_obj = {
                "t_netto": cart_dict[str(product.id)]["t_netto"],
                "t_brutto": cart_dict[str(product.id)]["t_brutto"],
                "total_netto": float(cart.get_total_price_netto()),
                "total": float(cart.get_total_price()),
                "len": cart.len(),
                "in_stock": product.qty - int(qty),
            }
            serialized = json.dumps(dict_obj)
            return HttpResponse(serialized)


class RemoveProduct(View):
    def post(self, request):
        if request.is_ajax():
            prod_id = request.POST.get("prod_id")
            qty = request.POST.get("qty")
            product = Products.objects.get(pk=int(prod_id))
            cart = Cart(request)
            cart.remove(product)

            dict_obj = {
                "total_netto": float(cart.get_total_price_netto()),
                "total": float(cart.get_total_price()),
                "len": cart.len(),
                "in_stock": product.qty + int(qty),
            }
            serialized = json.dumps(dict_obj)
            return HttpResponse(serialized)


class CartDetails(View):
    def get(self, request):
        pay_methods = PayMethod.objects.filter(is_active=True)
        delivery_type = DELIVERY_TYPE
        cart = Cart(request)
        print(cart)
        categorys = Category.objects.filter(is_active=True)
        ctx = {
            "cart_ctx": cart,
            "categorys": categorys,
            "pay_methods": pay_methods,
            "delivery_type": delivery_type,
        }
        return render(request, "cart/cart_detail.html", ctx)


add_product = AddProductView.as_view()
cart_details = CartDetails.as_view()
remove_product = RemoveProduct.as_view()
edit_product = EditQtyProduct.as_view()

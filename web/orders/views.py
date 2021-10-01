from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponse
from web.models import Category, Store, Profile, Address, PayMethod, DeliveryMethod, Orders
from .functions import new_number
from .forms import OrderBigForm, OrderDetailsForm
from web.constans import DELIVERY_TYPE
from web.cart.cart import Cart

import json
from decimal import Decimal


import stripe
from django.conf import settings

from datetime import datetime

stripe.api_key = settings.STRIPE_SECRET_KEY


@method_decorator(login_required, name="dispatch")
class OrderDetails(View):
    def get(self, request):
        form = OrderDetailsForm()
        ctx = {
            'form': form
        }
        return render(request, "orders/order_details.html", ctx)

    def post(self, request):
        form = OrderDetailsForm(request.POST)
        cart = Cart(request)

        if form.is_valid():
            pay_method = PayMethod.objects.get(name=form.cleaned_data['payment_method'])
            delivery_method = DeliveryMethod.objects.get(name=form.cleaned_data['delivery_method'])
            request.session['pay_method'] = pay_method.id
            request.session['delivery_method'] = delivery_method.id
        #     if delivery_method.inpost_box:
        #         return render(request, "orders/inpost_box.html")
        inpost_box_id = None
        if request.is_ajax():
            if 'inpost_box_id' in request.POST:
                inpost_box_id = request.POST.get('inpost_box_id')
                request.session['inpost_box_id'] = inpost_box_id
                
        
        today = datetime.now()
        store = Store.objects.all().first()
        order = Orders()
        order.number = new_number(store.id, day=today.day, month=today.month, year=today.year)
        order.store = store
        order.client = request.user
        order.phone_number = request.user.profile.phone_number
        order.delivery_method = DeliveryMethod.objects.get(id=int(request.session['delivery_method']))
        order.pay_method = PayMethod.objects.get(id=int(request.session['pay_method']))
        # order.inpost_box = inpost_box_id
        order.total_price = float(order.delivery_method.price) + float(cart.get_total_price())
        order.save()
        
        # response = redirect('checkout', order_id=order.id)
        # return response
        if order.delivery_method.inpost_box:
            return redirect('inpost_box', order_id=order.id)
        return redirect('checkout', order_id=order.id)
        


@method_decorator(login_required, name="dispatch")
class InpostBoxSearchView(View):
    def get(self, request, order_id):
        ctx = {'order_id': order_id}
        return render(request, "orders/inpost_box.html", ctx)

    def post(self, request, order_id):
        # session_dict = (request.session.get(str(request.user.id)))
        # delivery_type = DeliveryMethod.objects.filter(is_active=True)
        # pay_methods = PayMethod.objects.filter(is_active=True)
        # try:
        #     payment_set = PayMethod.objects.get(pk=session_dict['payment_id'])
        #     payment_default = PayMethod.objects.get(
        #         pk=int(session_dict['payment_id']))
        # except:
        #     payment_default = pay_methods.filter(default=True).first()
        #     payment_set = payment_default
        # try:
        #     delivery_set = DeliveryMethod.objects.get(
        #         pk=session_dict['delivery_id'])
        #     delivery_default = DeliveryMethod.objects.get(
        #         pk=int(session_dict['delivery_id']))
        # except:
        #     delivery_default = delivery_type.filter(default=True).first()
        #     delivery_set = delivery_default
        # try:
        #     payment_set = PayMethod.objects.get(pk=session_dict['payment_id'])
        #     payment_default = PayMethod.objects.get(
        #         pk=int(session_dict['payment_id']))
        # except:
        #     payment_set = payment_default

        # try:
        #     delivery_set = DeliveryMethod.objects.get(
        #         pk=session_dict['delivery_id'])
        #     delivery_default = DeliveryMethod.objects.get(
        #         pk=int(session_dict['delivery_id']))
        # except:
        #     delivery_set = delivery_default

        # try:
        #     inpost_box_id = session_dict['inpost_box_id']
        # except:
        #     inpost_box_id = False
        # if 'inpost_box_id' in request.POST:
        #     inpost_box_id = request.POST.get('inpost_box_id')
        #     request.session['inpost_box_id'] = inpost_box_id

        #     request.session[str(request.user.id)] = {
        #         'payment_id': str(delivery_default.id),
        #         'delivery_id': str(delivery_default.id),
        #         'inpost_box_id': inpost_box_id
        #     }
        return redirect('checkout', order_id=order_id)
        # return redirect('order_details', order_id=order_id )


class CheckOutDetails(View):
    def get(self, request, order):
        order = Orders.objects.get(pk=order)
        order_price = int(order.total_price * 100)
        ctx = {
            'order': order,
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
            'order': order
        }
        return render(request, "orders/checkout.html", ctx)

    def post(self, request, order):
        order = Orders.objects.get(pk=order)
        order_price = int(order.total_price * 100)
        checkout_session = stripe.checkout.Session.create(
            customer_email=request.user.email,
            payment_method_types=['card', 'p24'],
            line_items=[{
                'price_data': {
                    'currency': 'pln',
                    'unit_amount': order_price,
                    'product_data': {
                        'name':
                        'Zamówienie nr :' + order.number,
                        'images': [
                            "https://pieczatki-colop.com/media/images/bcg-stamp_LrTJcQE_YRKH6ut.webp"
                        ],
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://pieczatki-colop.com/',
            cancel_url="https://pieczatki-colop.com/zamowienia/platnosci/" +
            str(order.id) + "/",
        )
        return JsonResponse({'id': checkout_session.id})

       
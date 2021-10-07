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
            bill_select = form.cleaned_data['bill_select']
            pay_method = PayMethod.objects.get(
                name=form.cleaned_data['payment_method'])
            delivery_method = DeliveryMethod.objects.get(
                name=form.cleaned_data['delivery_method'])
            request.session['pay_method'] = pay_method.id
            request.session['delivery_method'] = delivery_method.id

            if request.is_ajax():
                if 'inpost_box_id' in request.POST:
                    inpost_box_id = request.POST.get('inpost_box_id')
                    request.session['inpost_box_id'] = inpost_box_id
            inpost_box_id = None

            today = datetime.now()
            store = Store.objects.all().first()
            order = Orders()
            order.number = new_number(
                store.id, day=today.day, month=today.month, year=today.year)
            order.store = store
            order.client = request.user
            order.phone_number = request.user.profile.phone_number
            order.delivery_method = DeliveryMethod.objects.get(
                id=int(request.session['delivery_method']))
            order.pay_method = PayMethod.objects.get(
                id=int(request.session['pay_method']))
            # order.inpost_box = inpost_box_id
            order.total_price = float(
                order.delivery_method.price) + float(cart.get_total_price())
            order.save()

            ctx = {'order': order}
            if delivery_method.inpost_box:
                return render(request, "orders/inpost_box.html", ctx)

            print(order.pay_method.pay_method)
            if order.pay_method.pay_method == 4:
                response = redirect('checkout', order=order.id)
                return response
            else:
                response = redirect('order_completed', order=order.id)
                return response
        else:
            messages.error(request, 'Wystąpił błąd')
            ctx = {
                'form': form
            }
            return render(request, "orders/order_details.html", ctx)


@method_decorator(login_required, name="dispatch")
class InpostBoxSearchView(View):
    def get(self, request, order):
        ctx = {'order_id': order}
        return render(request, "orders/inpost_box.html", ctx)

    def post(self, request, order):
        order = Orders.objects.get(pk=order)
        if order.pay_method.pay_method == '4':
            return redirect('checkout', order=order.id)
        else:
            return redirect('order_completed', order=order.id)


class OrderCompleted(View):
    def get(self, request, order):
        order = Orders.objects.get(pk=order)
        cart = Cart(request)
        cart.clear()
        ctx = {
            'order': order
        }
        return render(request, "orders/order_completed.html", ctx)


order_completed = OrderCompleted.as_view()

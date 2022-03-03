from datetime import datetime

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from web.cart.cart import Cart
from web.models import DeliveryMethod, Orders, Invoices, PayMethod, Store, ActivateToken

from .forms import OrderDetailsForm
from .functions import create_pdf_invoice, new_number, order_pay_status, order_inpost_box, new_invoice_number, send_email_order_completed

stripe.api_key = settings.STRIPE_SECRET_KEY


@method_decorator(login_required, name="dispatch")
class OrderDetails(View):
    def get(self, request):
        if request.user.profile.company:
            form = OrderDetailsForm(initial={"bill_select": "2"})
        else:
            form = OrderDetailsForm()
        ctx = {"form": form}
        return render(request, "orders/order_details.html", ctx)

    def post(self, request):
        form = OrderDetailsForm(request.POST)
        cart = Cart(request)
        inpost_box_id = None
        if request.is_ajax():
            if "inpost_box_id" in request.POST:
                inpost_box_id = request.POST.get("inpost_box_id")
                request.session["inpost_box_id"] = inpost_box_id

        if form.is_valid():
            pay_method = PayMethod.objects.get(
                name=form.cleaned_data["payment_method"])
            delivery_method = DeliveryMethod.objects.get(
                name=form.cleaned_data["delivery_method"]
            )
            request.session["pay_method"] = pay_method.id
            request.session["delivery_method"] = delivery_method.id

            today = datetime.now()
            store = Store.objects.all().first()
            order = Orders()
            order.number = new_number(
                store.id, day=today.day, month=today.month, year=today.year
            )
            order.store = store
            order.client = request.user
            order.pay_status = 2
            order.phone_number = request.user.profile.phone_number
            order.delivery_method = delivery_method
            order.pay_method = pay_method
            if delivery_method.inpost_box:
                order.pay_method = PayMethod.objects.get(pay_method=4)
            order.invoice_true = True if form.cleaned_data["bill_select"] == "2" else False
            order.total_price = float(delivery_method.price) + float(
                cart.get_total_price()
            )
            order.save()
            ctx = {"order": order}
            if delivery_method.inpost_box:
                return render(request, "orders/inpost_box.html", ctx)

            if pay_method.pay_method == 4:
                response = redirect("checkout", order=order.id)
                return response
            response = redirect("order_completed", order=order.id)
            return response
        else:
            messages.error(request, "Wystąpił błąd")
            ctx = {"form": form}
            return render(request, "orders/order_details.html", ctx)


@method_decorator(login_required, name="dispatch")
class InpostBoxSearchView(View):
    def get(self, request, order):
        ctx = {"order_id": order}
        return render(request, "orders/inpost_box.html", ctx)

    def post(self, request, order):
        order = Orders.objects.get(pk=order)
        if order.pay_method.pay_method == "4":
            return redirect("checkout", order=order.id)
        return redirect("order_completed", order=order.id)


@method_decorator(login_required, name="dispatch")
class OrderCompleted(View):
    def get(self, request, order):
        host = request.scheme + "://" + request.get_host()
        cart = Cart(request)
        order = Orders.objects.get(pk=order)
        order.status = 2
        if order.pay_method == "przelew p24":
            try:
                order.inpost_box = request.session["inpost_box_id"]
                del request.session["inpost_box_id"]
            except:
                pass
            order.main_status = 3
        if not order.products_item:
            order.products_item = cart.get_products()
        delivery_method = DeliveryMethod.objects.get(name=order.delivery_method)
        order_pay_status(order)
        order_inpost_box(request, order, delivery_method)
        if order.invoice_true and not order.invoice:
            file_name = create_pdf_invoice(order)
            send_email_order_completed(order, host, file_name=file_name)
        else:
            send_email_order_completed(order, host)
        cart.clear()
        order.save()
        ctx = {"order": order}
        if order.pay_status == 3:
            return render(request, "payments/checkout_success.html", ctx)
        return render(request, "orders/order_completed.html", ctx)



class RedirectFromOrderEmail(View):
    def get(self, request, token):
        try:
            user = ActivateToken.objects.get(activation_token=token).user
            login(request, user)
            return redirect("user_orders")
        except ActivateToken.DoesNotExist:
            messages.error(request, "Błędny token")
            return redirect("front_page")

order_details = OrderDetails.as_view()
inpost_box = InpostBoxSearchView.as_view()
order_completed = OrderCompleted.as_view()
redirect_from_email = RedirectFromOrderEmail.as_view()

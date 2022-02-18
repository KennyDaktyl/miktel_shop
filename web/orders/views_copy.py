from datetime import datetime

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views import View
from weasyprint import HTML

from web.cart.cart import Cart
from web.models import DeliveryMethod, Orders, Invoices, PayMethod, Store

from .forms import OrderDetailsForm
from .functions import create_pdf_invoice, new_number, new_invoice_number

stripe.api_key = settings.STRIPE_SECRET_KEY


@method_decorator(login_required, name="dispatch")
class OrderDetails(View):
    def get(self, request):
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
            order.phone_number = request.user.profile.phone_number
            order.delivery_method = delivery_method.name
            order.pay_method = PayMethod.objects.get(
                id=int(request.session["pay_method"])
            )
            order.pdf_created = True if form.cleaned_data["bill_select"] == "2" else False
            order.total_price = float(delivery_method.price) + float(
                cart.get_total_price()
            )
            order.save()

            ctx = {"order": order}
            if delivery_method.inpost_box:
                return render(request, "orders/inpost_box.html", ctx)

            if order.pay_method.pay_method == 4:
                response = redirect("checkout", order=order.id)
                return response
            else:
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
        if order.pay_method.pay_method == 4:
            return redirect("checkout", order=order.id)
        else:
            return redirect("order_completed", order=order.id)


class OrderCompleted(View):
    def get(self, request, order):
        cart = Cart(request)
        order = Orders.objects.get(pk=order)
        if order.pdf_created:
            invoice_number = new_invoice_number()
            invoice, created = Invoices.objects.get_or_create(pdf=invoice_number)
            invoice.number = invoice_number
            invoice.save()
            create_pdf_invoice(order, invoice, created)
        order.main_status = 2
        order.status = 2
        if not order.products_item:
            order.products_item = cart.get_products()
        delivery_method = DeliveryMethod.objects.get(name=order.delivery_method)
        if delivery_method.inpost_box and order.products_item.get(delivery_method.id):
            order.products_item.update(delivery_method.delivery_dict)
        order.save()
        cart.clear()
        ctx = {"order": order}
        return render(request, "orders/order_completed.html", ctx)


class CreateInvoice(View):
    def get(self, request, pk):
        order = Orders.objects.get(pk=pk)
        

        filename = f"faktura_{order.invoice_created.number}.pdf"
        context = {
            "order": order,
        }
        html_string = render_to_string("orders/invoice.html", context)

        html = HTML(string=html_string)
        html.write_pdf(target=settings.MEDIA_ROOT + f"/pdf/{filename}")

        fs = FileSystemStorage(settings.MEDIA_ROOT + "/pdf")
        with fs.open(settings.MEDIA_ROOT + f"/pdf/{filename}") as pdf:
            response = HttpResponse(
                pdf, content_type="application/pdf")
            response[
                "Content-Disposition"] = 'attachment; filename="{}"'.format(
                filename
            )
        return response


order_completed = OrderCompleted.as_view()
create_invoice = CreateInvoice.as_view()

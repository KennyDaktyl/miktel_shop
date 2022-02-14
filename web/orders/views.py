from operator import inv
from django_renderpdf.views import PDFView
from io import BytesIO
from unittest.mock import patch
from xml.etree.ElementInclude import include
from django.core.files import File
from django.template.loader import get_template
import tempfile
import os
from django.template.loader import render_to_string
from weasyprint import HTML
from django.core.files.storage import FileSystemStorage
import json
from datetime import datetime
from decimal import Decimal

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from web.cart.cart import Cart
from web.constans import DELIVERY_TYPE
from web.models import (
    Address,
    Category,
    DeliveryMethod,
    Orders,
    Invoices,
    PayMethod,
    Profile,
    Store,
)

from .forms import OrderBigForm, OrderDetailsForm
from .functions import new_number, render_to_pdf, create_pdf_invoice

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
                print(inpost_box_id)
                print("sdsds")

        if form.is_valid():
            bill_select = form.cleaned_data["bill_select"]
            pay_method = PayMethod.objects.get(
                name=form.cleaned_data["payment_method"]
            )
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
            order.delivery_method = DeliveryMethod.objects.get(
                id=int(request.session["delivery_method"])
            )
            order.pay_method = PayMethod.objects.get(
                id=int(request.session["pay_method"])
            )
            # order.inpost_box = inpost_box_id
            order.total_price = float(order.delivery_method.price) + float(
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
        order.main_status = 2
        order.status = 2
        order.products_item = cart.get_products()
        order.save()
        cart.clear()
        ctx = {"order": order}
        create_pdf_invoice(order)
        return render(request, "orders/order_completed.html", ctx)


class CreateInvoice(PDFView):
    template_name = 'orders/invoice.html'
    allow_force_html = True
    prompt_download = True
    download_name = "faktura.pdf"

    def get_context_data(self, *args, **kwargs):
        """Pass some extra context to the template."""
        context = super().get_context_data(*args, **kwargs)
        order = Orders.objects.get(pk=kwargs['pk'])
        invoice_number = (order.number).replace("/", "-")
        filename = f"faktura_{invoice_number}_WWW.pdf"
        invoice, created = Invoices.objects.get_or_create(
            pdf=filename)
        invoice_number = (order.number).replace("/", "-")
        if created:
            os.remove(os.path.join(
                settings.MEDIA_ROOT + "pdf/" + str(invoice.pdf)))
        order.pdf = invoice
        order.save()
        context['order'] = order
        context['invoice'] = invoice
        print(self.get_download_name())
        # invoice.pdf.save(filename, File(BytesIO(pdf.content)))
        return context

    #     filename = f"faktura_{invoice_number}_WWW.pdf"
    #     invoice, created = Invoices.objects.get_or_create(
    #         pdf=filename)
    #     if created:
    #         os.remove(os.path.join(
    #             settings.MEDIA_ROOT + "pdf/" + str(invoice.pdf)))
    #     invoice.pdf.save(filename, File(BytesIO(pdf.content)))
    #     order.pdf = invoice
    #     order.save()
    #     print(order.products_item)
    #     invoice.number = f"{invoice_number}_WWW"
    #     pdf = render_to_pdf('orders/invoice.html',
    #                         {'order': order, 'invoice': invoice})
    #     invoice.pdf.save(filename, File(BytesIO(pdf.content)))
    #     response = HttpResponse(invoice.pdf, content_type='application/pdf')
    #     response['Content-Disposition'] = f'filename={filename}'
    #     return response


order_completed = OrderCompleted.as_view()
create_invoice = CreateInvoice.as_view()

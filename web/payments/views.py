import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from rest_framework.views import APIView
from web.cart.cart import Cart
from web.models.orders import DeliveryMethod, Invoices, Orders
from web.orders.functions import create_pdf_invoice, new_invoice_number

stripe.api_key = settings.STRIPE_SECRET_KEY


@method_decorator(login_required, name="dispatch")
class CheckoutView(View):
    def get(self, request, order):
        order = Orders.objects.get(id=order)
        try:
            order.inpost_box = request.session["inpost_box_id"]
            order.save()
        except KeyError:
            pass
        intent = stripe.PaymentIntent.create(
            amount=order.get_total_price_stripe(),
            currency="pln",
            payment_method_types=["p24"],
            receipt_email=request.user.email,
        )
        order.payment_intent = intent["id"]
        order.save()
        ctx = {
            "order": order,
            "PAYMENT_INTENT_CLIENT_SECRET": intent["client_secret"],
            "PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
        }
        return render(request, "payments/checkout.html", ctx)


@method_decorator(csrf_exempt, name="dispatch")
class PaymentIntentView(View):
    def post(self, request):
        try:
            intent = stripe.PaymentIntent.create(
                amount=1099,
                currency="pln",
                payment_method_types=["p24"],
            )
            return JsonResponse({"clientSecret": intent["client_secret"]})
        except Exception:
            return HttpResponse(status=403)


@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        payload = request.body
        try:
            sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", None)
            event = stripe.Webhook.construct_event(
                payload=payload,
                sig_header=sig_header,
                secret=settings.STRIPE_ENDPOINT_SECRET,
            )
            if event.type == "payment_intent.succeeded":
                # payment_intent_id = event.data.object["id"]
                # order = Orders.objects.get(payment_intent="pi_3O2Wt9EgeezQE8SP1GzldGzA")
                # order.pay_status = 3
                # order.payment_success = True
                # order.save()

                print(event)
        except ValueError as e:
            print(e)
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            print(e)
            return HttpResponse(status=400)

        # if event.type == "payment_intent.succeeded":
        #     payment_intent = (
        #         event.data.object
        #     )  # contains a stripe.PaymentIntent
        #     print("PaymentIntent was successful!")
        # elif event.type == "payment_method.attached":
        #     payment_method = (
        #         event.data.object
        #     )  # contains a stripe.PaymentMethod
        #     print("PaymentMethod was attached to a Customer!")
        # # ... handle other event types
        # else:
        #     print("Unhandled event type {}".format(event.type))

        return HttpResponse(status=200)


@method_decorator(login_required, name="dispatch")
class PayMentSuccessView(View):
    def get(self, request, order):
        cart = Cart(request)
        order = Orders.objects.get(id=order)
        order.pay_status = 3
        order.status = 2
        order.payment_success = True
        if order.pdf_created:
            invoice_number = new_invoice_number()
            invoice, created = Invoices.objects.get_or_create(pdf=invoice_number)
            invoice.number = invoice_number
            invoice.save()
            create_pdf_invoice(order, invoice, created)
        if not order.products_item:
            order.products_item = cart.get_products()
        delivery_method = DeliveryMethod.objects.get(name=order.delivery_method)
        if delivery_method.inpost_box and not order.products_item.get(
            delivery_method.id
        ):
            order.products_item.update(delivery_method.delivery_dict)
        order.save()
        cart.clear()
        ctx = {"order": order}
        return render(request, "payments/checkout_success.html", ctx)


checkout = CheckoutView.as_view()
payment_intent = PaymentIntentView.as_view()
stripe_webhook = StripeWebhookView.as_view()

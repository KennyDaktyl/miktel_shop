from web.cart.my_context_processor import cart
from web.models.orders import Orders
from django import views
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework import permissions

from web.cart.cart import Cart

import stripe
import json

from datetime import datetime

from stripe.api_resources import payment_intent
stripe.api_key = settings.STRIPE_SECRET_KEY


@method_decorator(login_required, name="dispatch")
class CheckoutView(View):
    def get(self, request, order):
        order = Orders.objects.get(id=order)
        try:
            order.inpost_box = request.session['inpost_box_id']
            order.save()
            del request.session['inpost_box_id']
        except:
            pass
        intent = stripe.PaymentIntent.create(
            amount=order.get_total_price_stripe(),
            currency='pln',
            payment_method_types=['p24'],
            receipt_email=request.user.email,
        )
        ctx = {'order': order,
               'PAYMENT_INTENT_CLIENT_SECRET': intent['client_secret']}
        return render(request, "payments/checkout.html", ctx)


@method_decorator(login_required, name="dispatch")
class PayMentSuccessView(View):
    def get(self, request, order):
        order = Orders.objects.get(id=order)
        order.main_status = 3
        order.status = 2
        order.save()

        cart = Cart(request)
        cart.clear()
        return render(request, "payments/checkout_success.html")


@method_decorator(csrf_exempt, name='dispatch')
class PaymentIntentView(View):
    def post(self, request):
        try:
            intent = stripe.PaymentIntent.create(
                amount=1099,
                currency='pln',
                payment_method_types=['p24'],
            )
            return JsonResponse({'clientSecret': intent['client_secret']})
        except Exception as e:
            return HttpResponse(status=403)


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        payload = request.body
        try:
            sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', None)
            event = stripe.Webhook.construct_event(
                payload=payload, sig_header=sig_header, secret=settings.STRIPE_ENDPOINT_SECRET
            )
            print(event)
        except ValueError as e:
            print(e)
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            print(e)
            return HttpResponse(status=400)

        # # Handle the event
        # if event.type == 'payment_intent.succeeded':
        #     payment_intent = event.data.object # contains a stripe.PaymentIntent
        #     print('PaymentIntent was successful!')
        # elif event.type == 'payment_method.attached':
        #     payment_method = event.data.object # contains a stripe.PaymentMethod
        #     print('PaymentMethod was attached to a Customer!')
        # # ... handle other event types
        # else:
        #     print('Unhandled event type {}'.format(event.type))

        return HttpResponse(status=200)


checkout = CheckoutView.as_view()
payment_success = PayMentSuccessView.as_view()
payment_intent = PaymentIntentView.as_view()
stripe_webhook = StripeWebhookView.as_view()

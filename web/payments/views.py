from django import views
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from rest_framework.views import APIView


import stripe
import json

from datetime import datetime

from stripe.api_resources import payment_intent
stripe.api_key = settings.STRIPE_SECRET_KEY

@method_decorator(login_required, name="dispatch")
class PaymentIntentView(View):
    def get(self, request):
        
        stripe.PaymentIntent.create(
            amount=1099,
            currency='pln',
            payment_method_types=['p24'],
        )

        ctx = {
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
        }
        return render(request, "payments/payment_intent.html", ctx)

endpoint_secret =  settings.STRIPE_ENDPOINT_SECRET

@csrf_protect
class StripeWebhookView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(status=400)

        # Handle the event
        if event.type == 'payment_intent.succeeded':
            payment_intent = event.data.object # contains a stripe.PaymentIntent
            print('PaymentIntent was successful!')
        elif event.type == 'payment_method.attached':
            payment_method = event.data.object # contains a stripe.PaymentMethod
            print('PaymentMethod was attached to a Customer!')
        # ... handle other event types
        else:
            print('Unhandled event type {}'.format(event.type))

        return HttpResponse(status=200)


payment_intent = PaymentIntentView.as_view()
stripe_webhook = StripeWebhookView
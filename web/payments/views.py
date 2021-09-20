from django import views
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

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

@csrf_protect
class StripeWebhookView(views):
    def post(self, request):
        payload = request.body
        event = None

        try:
            event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
            )
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)

        # Handle the event
        if event.type == 'payment_intent.succeeded':
            payment_intent = event.data.object # contains a stripe.PaymentIntent
           
            # Then define and call a method to handle the successful payment intent.
            # handle_payment_intent_succeeded(payment_intent)
        elif event.type == 'payment_method.attached':
            payment_method = event.data.object # contains a stripe.PaymentMethod
            # Then define and call a method to handle the successful attachment of a PaymentMethod.
            # handle_payment_method_attached(payment_method)
        # ... handle other event types
        else:
            print('Unhandled event type {}'.format(event.type))

        return HttpResponse(status=200)

payment_intent = PaymentIntentView.as_view()
stripe_webhook = StripeWebhookView.as_view()
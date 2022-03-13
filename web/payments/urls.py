from django.urls import path

from .views import checkout, payment_intent, stripe_webhook

urlpatterns = [
    path("checkout/<int:order>", checkout, name="checkout"),
    path("payment_intent", payment_intent, name="payment_intent"),
    path("webhook", stripe_webhook, name="stripe_webhook"),
]

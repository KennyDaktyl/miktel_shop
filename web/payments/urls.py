from django.urls import path
from .views import *

urlpatterns = [
    path('checkout', checkout, name='checkout'),
    path('payment_intent', payment_intent, name='payment_intent'),
    path('webhook', stripe_webhook, name='stripe_webhook'),
]

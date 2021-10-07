from django.urls import path
from .views import *

urlpatterns = [
    path('checkout/<int:order>', checkout, name='checkout'),
    path('payment_success', payment_success, name='payment_success'),
    path('payment_intent', payment_intent, name='payment_intent'),
    path('webhook', stripe_webhook, name='stripe_webhook'),
]

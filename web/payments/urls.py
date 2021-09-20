from django.urls import path
from .views import *

urlpatterns = [
    path('payment_intent', payment_intent, name='payment_intent'),
    path('webhook', stripe_webhook, name='stripe_webhook'),
]

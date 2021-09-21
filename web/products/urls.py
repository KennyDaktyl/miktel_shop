from django.urls import path
from django.conf import settings
from .views import *

urlpatterns = [
    path('kategorie/<slug:slug>', products_category, name='products_category'),
    # path('kategorie/<slug:slug>',
    #      CategoryDetails.as_view(),
    #      name='category_details'),
]

from django.urls import path
from django.conf import settings
from .views import *

urlpatterns = [
    path('<slug:cat>/<slug:sub_cat>', sub_category_items, name='sub_category_items'),
    path('<slug:cat>/<slug:sub_cat>/<slug:product>', product_details, name='product_details'),
    path('sklep_online', shop_main_view, name='shop_main_view'),
    # path('kategorie/<slug:slug>',
    #      CategoryDetails.as_view(),
    #      name='category_details'),
]

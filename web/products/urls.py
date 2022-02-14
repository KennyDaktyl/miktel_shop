from django.conf import settings
from django.urls import path

from .views import *

urlpatterns = [
    path("", shop_main_view, name="shop_main_view"),
    path("szukaj", search_products, name="search_products"),
    path("szukaj_js", search_products_js, name="search_products_js"),
    path(
        "produkty/<slug:cat>/<slug:sub_cat>/<int:pk>",
        sub_category_products,
        name="sub_category_products",
    ),
    path(
        "produkty/<slug:cat>/<slug:sub_cat>/<slug:sub_cat_type>/<int:pk>",
        sub_category_type,
        name="sub_category_type_products",
    ),
    path(
        "produkty/<slug:cat>/<slug:sub_cat>/<slug:sub_cat_type>/<slug:product>/<int:pk>",
        product_details,
        name="product_details",
    ),
    # path('kategorie/<slug:slug>',
    #      CategoryDetails.as_view(),
    #      name='category_details'),
]

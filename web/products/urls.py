from django.urls import path

from .views import (
    product_details,
    search_products,
    search_products_js,
    shop_main_view,
    sub_category_products,
    sub_category_type,
)

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
]

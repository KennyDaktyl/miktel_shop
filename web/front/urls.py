from django.urls import path

from .views import (
    first_page,
    contact_page,
    index_citys_stamp_delivery,
    privacy_policy,
    terms_rules,
    index_city_detail_stamp_delivery,
    city_details_stamp_delivery,
)

urlpatterns = [
    path("", first_page, name="front_page"),
    path("kontakt", contact_page, name="contact_page"),
    path("polityka-prywatnosci", privacy_policy, name="privacy_policy"),
    path("regulamin", terms_rules, name="terms"),
    path(
        "wyrob-pieczatek-wysylka-lista-miast",
        index_citys_stamp_delivery,
        name="index_citys_stamp_delivery",
    ),
    path(
        "wyrob-pieczatek-online-do-miast-na-<slug:slug>/<int:pk>",
        index_city_detail_stamp_delivery,
        name="index_city_detail_stamp_delivery",
    ),
    path(
        "wyrob-pieczatek-online-w-<slug:slug>/<int:pk>",
        city_details_stamp_delivery,
        name="city_details_stamp_delivery",
    ),
]

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import *

# CartDetails,
urlpatterns = [
    path("dodaj_produkt/", add_product, name="add_product"),
    path("zmien_ilosc/", EditQtyProduct.as_view(), name="change_qty"),
    path("usun_produkt/", RemoveProduct.as_view(), name="del_product"),
    path("podsumowanie/", CartDetails.as_view(), name="cart_details"),
]

from django.urls import path

from .views import add_product, cart_details, remove_product, edit_product

urlpatterns = [
    path("dodaj_produkt/", add_product, name="add_product"),
    path("zmien_ilosc/", edit_product, name="change_qty"),
    path("usun_produkt/", remove_product, name="del_product"),
    path("podsumowanie/", cart_details, name="cart_details"),
]

from django.conf.urls.static import static
from django.urls import path

from .views import order_completed, order_details, inpost_box, redirect_from_email

# CartDetails,
urlpatterns = [
    path("podsumowanie/", order_details, name="order_details"),
    path(
        "podsumowanie/wybierz_paczkomat/<int:order>",
        inpost_box,
        name="inpost_box",
    ),
    path(
        "zamowienie_zakonczono/<int:order>",
        order_completed,
        name="order_completed",
    ),
     path(
        "redirect_from_email/<token>", redirect_from_email, name="redirect_from_email"
    ),
]

from django.conf.urls.static import static
from django.urls import path

from .views import *

# CartDetails,
urlpatterns = [
    path("podsumowanie/", OrderDetails.as_view(), name="order_details"),
    path(
        "podsumowanie/wybierz_paczkomat/<int:order>",
        InpostBoxSearchView.as_view(),
        name="inpost_box",
    ),
    path(
        "zamowienie_zakonczono/<int:order>",
        order_completed,
        name="order_completed",
    ),
    # path(
    #     "create_invoice/<int:pk>",
    #     create_invoice,
    #     name="create_invoice",
    # ),
]

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import *

# CartDetails,
urlpatterns = [
    path('podsumowanie/', OrderDetails.as_view(), name='order_details'),
    path('podsumowanie/wybierz_paczkomat/<int:order>',
         InpostBoxSearchView.as_view(),
         name='inpost_box'),
    path('zamowienie_zakonczono/<int:order>',
         order_completed,
         name='order_completed'),
]

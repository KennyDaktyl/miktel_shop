from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("web.front.urls")),
    path("accounts/", include("web.accounts.urls")),
    path("koszyk/", include("web.cart.urls")),
    path("zamowienia/", include("web.orders.urls")),
    path("payment/", include("web.payments.urls")),
    path("produkty/", include("web.products.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

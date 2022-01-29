from email.mime import image
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.conf.urls import include, url
from django.urls import path
from django.views.generic import TemplateView
from django.conf.urls import handler404, handler500
from web.front.views import error404, error500

from .sitemaps import *

sitemaps = {
    'static': StaticViewSitemap,
    'product_details': ProductDetailsSiteView,
    'sub_category_details': SubCategoryDetailsSiteView,
    'sub_category_type_details': SubCategoryTypeDetailsSiteView
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    url(
        r'^robots\.txt$',
        TemplateView.as_view(template_name="front_page/robots.txt",
                             content_type='text/plain')),

    path("", include("web.front.urls")),
    path("accounts/", include("web.accounts.urls")),
    path("koszyk/", include("web.cart.urls")),
    path("zamowienia/", include("web.orders.urls")),
    path("payment/", include("web.payments.urls")),
    path("sklep_online/", include("web.products.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = error404
handler404 = error404

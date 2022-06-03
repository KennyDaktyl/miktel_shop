from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import views
from django.contrib.sitemaps import views as sitemaps_views
from django.views.decorators.cache import cache_page
from django.conf.urls import include
from django.urls import path
from django.views.generic import TemplateView
from web.front.views import error_404, error_500
from web.products.views import redirect_product, redirect_sub_category, \
    redirect_sub_category_type

from .sitemaps import (
    StaticViewSitemap,
    ProductDetailsSiteView,
    SubCategoryDetailsSiteView,
    SubCategoryTypeDetailsSiteView,
    ArticleDetailsSiteView,
    CitysIndexStampListView,
    CityIndexStampDetailsView
)

sitemaps = {
    "static": StaticViewSitemap,
    "product_details": ProductDetailsSiteView,
    "sub_category_details": SubCategoryDetailsSiteView,
    "sub_category_type_details": SubCategoryTypeDetailsSiteView,
    "article_details": ArticleDetailsSiteView,
}

sitemaps_cities_shipping_stamp = {
    "citys_stamp_delivery": CitysIndexStampListView,
    "city_stamp_delivery_details": CityIndexStampDetailsView
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("admin/clearcache/", include("clearcache.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path(
        "sitemaps_cities_shipping_stamp.xml",
        cache_page(86400)(views.index),
        {"sitemaps": sitemaps_cities_shipping_stamp,
            'sitemap_url_name': 'sitemaps_cities_shipping_stamp'},
    ),
    path('sitemaps_cities_shipping_stamp-<section>.xml',
         cache_page(86400)(views.sitemap),
         {'sitemaps': sitemaps_cities_shipping_stamp}, name='sitemaps_cities_shipping_stamp'),
    path('sitemap.xml',
         cache_page(86400)(sitemaps_views.index),
         {'sitemaps': sitemaps, 'sitemap_url_name': 'sitemaps'}),
    path('sitemap-<section>.xml',
         cache_page(86400)(sitemaps_views.sitemap),
         {'sitemaps': sitemaps}, name='sitemaps'),
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="front_page/robots.txt", content_type="text/plain"
        ),
    ),
    path("", include("web.front.urls")),
    path("accounts/", include("web.accounts.urls")),
    path("koszyk/", include("web.cart.urls")),
    path("zamowienia/", include("web.orders.urls")),
    path("payment/", include("web.payments.urls")),
    path("produkty/", include("web.products.urls")),
    path("blog/", include("web.articles.urls")),
    path(
        "sklep_online/produkty/<slug:cat>/<slug:sub_cat>/<slug:sub_cat_type>/<slug:product>/<int:pk>",
        redirect_product,
        name="redirect-products",
    ),
    path(
        "sklep_online/produkty/<slug:cat>/<slug:sub_cat>/<int:pk>",
        redirect_sub_category,
        name="redirect_sub_category",
    ),
    path(
        "sklep_online/produkty/<slug:cat>/<slug:sub_cat>/<slug:sub_cat_type>/<int:pk>",
        redirect_sub_category_type,
        name="redirect_sub_category_type",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = error_404
handler500 = error_500

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.conf.urls import include, url
from django.urls import path
from django.views.generic import TemplateView
from web.front.views import error_404, error_500
from web.products.views import redirect_product

from .sitemaps import (
    StaticViewSitemap,
    ProductDetailsSiteView,
    SubCategoryDetailsSiteView,
    SubCategoryTypeDetailsSiteView,
    ArticleDetailsSiteView,
)

sitemaps = {
    "static": StaticViewSitemap,
    "product_details": ProductDetailsSiteView,
    "sub_category_details": SubCategoryDetailsSiteView,
    "sub_category_type_details": SubCategoryTypeDetailsSiteView,
    "article_details": ArticleDetailsSiteView,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path('admin/clearcache/', include('clearcache.urls')),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    url(
        r"^robots\.txt$",
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

    path("sklep_online/produkty/<slug:cat>/<slug:sub_cat>/<slug:sub_cat_type>/<slug:product>/<int:pk>", redirect_product, name="redirect-products")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = error_404
handler500 = error_500

import imp
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from web.models import Products
from web.models.products import SubCategory, SubCategoryType
from web.models.articles import Articles
from web.models.orders import IndexAlfaStamp, Citys


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "daily"

    def items(self):
        return [
            "front_page",
            "shop_main_view",
            "cart_details",
            "stripe_webhook",
            "contact_page",
            "articles_list",
            "privacy_policy",
            "terms",
            "index_citys_stamp_delivery"
        ]

    def location(self, item):
        return reverse(item)


class SubCategoryDetailsSiteView(Sitemap):
    priority = 0.5
    changefreq = "weekly"
    protocol = "https"

    def items(self):
        return SubCategory.objects.all()

    def location(self, items):
        return reverse(
            "sub_category_products",
            kwargs={
                "cat": items.category.slug,
                "sub_cat": items.slug,
                "pk": items.pk,
            },
        )


class SubCategoryTypeDetailsSiteView(Sitemap):
    priority = 0.5
    changefreq = "weekly"
    protocol = "https"

    def items(self):
        return SubCategoryType.objects.all()

    def location(self, items):
        return reverse(
            "sub_category_type_products",
            kwargs={
                "cat": items.sub_category.category.slug,
                "sub_cat": items.sub_category.slug,
                "sub_cat_type": items.slug,
                "pk": items.pk,
            },
        )


class ProductDetailsSiteView(Sitemap):
    priority = 1.0
    changefreq = "always"
    protocol = "https"

    def items(self):
        return Products.objects.filter(is_active=True)

    def location(self, items):
        return reverse(
            "product_details",
            kwargs={
                "sub_cat": items.sub_category_type.sub_category.slug,
                "product": items.slug,
                "pk": items.pk,
            },
        )


class ArticleDetailsSiteView(Sitemap):
    priority = 1.0
    changefreq = "always"
    protocol = "https"

    def items(self):
        return Articles.objects.all()

    def location(self, items):
        return reverse(
            "article_details",
            kwargs={
                "category": items.category.slug,
                "title": items.slug,
                "pk": items.pk,
            },
        )


class CitysIndexStampListView(Sitemap):
    priority = 1.0
    changefreq = "always"
    protocol = "https"

    def items(self):
        return IndexAlfaStamp.objects.all()

    def location(self, items):
        return reverse(
            "index_city_detail_stamp_delivery",
            kwargs={
                "slug": items.slug,
                "pk": items.pk,
            },
        )


class CityIndexStampDetailsView(Sitemap):
    priority = 1.0
    changefreq = "always"
    protocol = "https"
    limit = 10000

    def items(self):
        return Citys.objects.all()

    def location(self, items):
        return reverse(
            "city_details_stamp_delivery",
            kwargs={
                "slug": items.slug,
                "pk": items.pk,
            },
        )

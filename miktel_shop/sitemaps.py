from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from web.models import Products
from web.models.products import SubCategory, SubCategoryType


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['front_page', 'shop_main_view', 'cart_details', 'stripe_webhook', 'contact_page']

    def location(self, item):
        return reverse(item)

class SubCategoryDetailsSiteView(Sitemap):
    priority = 0.5
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return SubCategory.objects.all()


    def location(self, items):
        return reverse("sub_category_products",
                       kwargs={
                           "cat": items.category.slug,
                           "sub_cat": items.slug,
                       })

class SubCategoryTypeDetailsSiteView(Sitemap):
    priority = 0.5
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return SubCategoryType.objects.all()


    def location(self, items):
        return reverse("sub_category_type_products",
                       kwargs={
                           "cat": items.sub_category.category.slug,
                           "sub_cat": items.sub_category.slug,
                           "sub_cat_type": items.slug,
                       })


class ProductDetailsSiteView(Sitemap):
    priority = 1.0
    changefreq = 'always'
    protocol = 'https'

    def items(self):
        return Products.objects.filter(is_active=True)


    def location(self, items):
        return reverse("product_details",
                       kwargs={
                           "cat": items.sub_category_type.sub_category.category.slug,
                           "sub_cat": items.sub_category_type.sub_category.slug,
                           "sub_cat_type": items.sub_category_type.slug,
                           "product": items.slug,
                       })

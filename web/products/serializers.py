from rest_framework import serializers
from web.models import Products


class ProductSerializer(serializers.ModelSerializer):
    product_url = serializers.URLField(
        source='get_absolute_url', read_only=True)

    class Meta:
        model = Products
        depth = 3
        fields = ('name', 'sub_category_type', 'id',
                  'price_promo', 'price', 'slug', 'product_url', 'image')
        ordering_fields = "__all__"
        ordering = (
            "name",
        )

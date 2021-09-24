from rest_framework import serializers
from web.models import Products

class ProductSerializer(serializers.ModelSerializer):
    product_url = serializers.URLField(source='get_absolute_url', read_only=True) 

    class Meta:
        model = Products
        depth = 3
        fields = '__all__' 
        ordering_fields = "__all__"
        ordering = (
            "name",
        )


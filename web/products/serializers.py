from rest_framework import serializers
from web.models import Products
from web.models.products import Category, SubCategory, SubCategoryType, Images, Vat


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        depth = 1
        fields = ("name", "id", "slug")
        ordering = ("name",)


class SubCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = SubCategory
        depth = 1
        fields = ("name", "category", "id", "slug")
        ordering = ("name",)


class SubCategoryTypeSerializer(serializers.ModelSerializer):
    sub_category = SubCategorySerializer(read_only=True)

    class Meta:
        model = SubCategoryType
        depth = 1
        fields = ("name", "sub_category", "id", "slug")
        ordering = ("name",)


class ImagesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Images
        depth = 1
        fields = ["id", "image"]
        ordering = ("image",)


class VatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vat
        depth = 1
        fields = ("id", "name")


class ProductSerializer(serializers.ModelSerializer):
    product_url = serializers.URLField(source="get_absolute_url", read_only=True)
    sub_category_type = SubCategoryTypeSerializer(read_only=True)
    tax = VatSerializer()

    class Meta:
        model = Products
        depth = 2
        fields = (
            "name",
            "sub_category_type",
            "id",
            "price_promo",
            "price",
            "slug",
            "qty",
            "product_url",
            "image",
            "tax",
        )
        ordering_fields = "__all__"
        ordering = ("name",)

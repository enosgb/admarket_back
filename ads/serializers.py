from rest_framework import serializers

from .models import Ad, Category, Product, ProductImage, Store


# Categories
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CategorySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "image")


# Products
class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySimpleSerializer(read_only=True)
    main_image = serializers.ImageField(
        source="main_image.0.image",
        read_only=True,
    )

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "active",
            "category",
            "main_image",
            "stock",
            "cost_price",
            "sale_price",
        )


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "active",
            "category",
            "stock",
            "cost_price",
            "sale_price",
        )


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("id", "image", "is_main")


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySimpleSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "active",
            "category",
            "images",
            "stock",
            "cost_price",
            "sale_price",
            "created_at",
            "updated_at",
        )


class ProductImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("id", "image", "is_main")

    def validate(self, attrs):
        product = self.context["product"]

        if attrs.get("is_main", False):
            if ProductImage.objects.filter(
                product=product,
                is_main=True,
            ).exists():
                raise serializers.ValidationError(
                    {"is_main": "Este produto já possui uma imagem principal."}
                )
        return attrs


class ProductSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "sale_price"]


# Stores
class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"


# ADS


class AdSerializer(serializers.ModelSerializer):
    product = ProductSimpleSerializer(read_only=True)

    class Meta:
        model = Ad
        fields = "__all__"

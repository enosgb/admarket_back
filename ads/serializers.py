from rest_framework import serializers

from .models import Category, Product, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CategorySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "image")


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

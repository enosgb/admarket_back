from rest_framework import serializers

from .models import Ad, Category, Favorite, Product, ProductImage, Store


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
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("id", "image", "is_main")


class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySimpleSerializer(read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "active",
            "description",
            "category",
            "image",
            "stock",
            "cost_price",
            "sale_price",
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get("request")
        if request and not (request.user and request.user.is_staff):
            rep.pop("cost_price", None)
        return rep


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySimpleSerializer(read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "active",
            "category",
            "image",
            "stock",
            "cost_price",
            "sale_price",
            "created_at",
            "updated_at",
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get("request")
        if request and not (request.user and request.user.is_staff):
            rep.pop("cost_price", None)
        return rep


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "active",
            "image",
            "category",
            "stock",
            "cost_price",
            "sale_price",
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


class ProductSimpleWithMainImageSerializer(serializers.ModelSerializer):
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "name", "sale_price", "main_image"]

    def get_main_image(self, obj):
        if hasattr(obj, "main_image") and obj.main_image:
            return obj.main_image[0].image.url
        return None


# Stores
class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"


# ADS


class AdSerializer(serializers.ModelSerializer):
    product = ProductSimpleWithMainImageSerializer(read_only=True)

    class Meta:
        model = Ad
        fields = [
            "id",
            "title",
            "description",
            "active",
            "published",
            "store",
            "product",
            "created_at",
            "updated_at",
        ]


class AdDetailSerializer(serializers.ModelSerializer):
    product = ProductDetailSerializer(read_only=True)

    class Meta:
        model = Ad
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


# Favorites


class FavoriteSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )

    class Meta:
        model = Favorite
        fields = ["id", "user", "product", "product_id", "created_at"]
        read_only_fields = ["user", "created_at"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        favorite, created = Favorite.objects.get_or_create(**validated_data)
        return favorite

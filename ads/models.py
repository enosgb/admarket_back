from cloudinary_storage.storage import MediaCloudinaryStorage
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True, null=True)
    active = models.BooleanField(default=True)

    image = models.ImageField(
        upload_to="admaker/categories/images/",
        storage=MediaCloudinaryStorage(),
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["active"]),
        ]

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        "Product",
        on_delete=models.SET_NULL,
        related_name="images",
        blank=True,
        null=True,
    )

    image = models.ImageField(
        upload_to="admaker/products/images/",
        storage=MediaCloudinaryStorage(),
    )

    is_main = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["product", "is_main"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["product"],
                condition=models.Q(is_main=True),
                name="unique_main_image_per_product",
            )
        ]


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)

    category = models.ForeignKey(
        "Category",
        on_delete=models.PROTECT,
        related_name="products",
    )

    stock = models.PositiveIntegerField(default=0)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["active"]),
            models.Index(fields=["category"]),
            models.Index(fields=["stock"]),
            models.Index(fields=["cost_price"]),
            models.Index(fields=["sale_price"]),
            models.Index(fields=["active", "category"]),
        ]

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(
        upload_to="admaker/stores/images/",
        storage=MediaCloudinaryStorage(),
        blank=True,
        null=True,
    )
    active = models.BooleanField(default=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["active"]),
            models.Index(fields=["city"]),
            models.Index(fields=["state"]),
            models.Index(fields=["active", "city", "state"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return self.name


# ADS
class Ad(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    product = models.ForeignKey(
        "Product", on_delete=models.SET_NULL, related_name="ads", null=True, blank=True
    )
    store = models.ForeignKey(
        "Store", on_delete=models.SET_NULL, related_name="ads", null=True, blank=True
    )

    active = models.BooleanField(default=True)
    published = models.BooleanField(default=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["active"]),
            models.Index(fields=["published"]),
            models.Index(fields=["store"]),
            models.Index(fields=["product"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["active", "published"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Favorite(models.Model):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="favorites",
    )
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="favorited_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")
        indexes = [
            models.Index(fields=["user", "product"], name="idx_user_product"),
            models.Index(fields=["created_at"], name="idx_created_at"),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.product.name}"

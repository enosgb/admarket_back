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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["active"]),
            models.Index(fields=["category"]),
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

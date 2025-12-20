from cloudinary_storage.storage import MediaCloudinaryStorage
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.CharField(max_length=200, blank=True, null=True)
    active = models.BooleanField(default=True)
    image = models.ImageField(
        blank=True,
        null=True,
        upload_to="admaker/ads/categories/",
        storage=MediaCloudinaryStorage(),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

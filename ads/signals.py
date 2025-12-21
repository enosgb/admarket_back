# ads/signals.py
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Ad, Favorite, ProductImage


@receiver([post_save, post_delete], sender=Ad)
@receiver([post_save, post_delete], sender=ProductImage)
def clear_ads_cache(sender, **kwargs):
    cache.delete_pattern("views.decorators.cache.cache_*")


@receiver([post_save, post_delete], sender=Favorite)
def clear_favorites_cache(sender, **kwargs):
    cache.delete_pattern("views.decorators.cache.cache_*")

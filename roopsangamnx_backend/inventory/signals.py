from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from .models import Product, ProductVariant

# Invalidate cache when a product is added or modified
@receiver(post_save, sender=Product)
def clear_product_cache_on_save(sender, instance, **kwargs):
    print("Clear prod cache")
    cache.delete('product_list')
    cache.delete('filters')

# Invalidate cache when a product is deleted
@receiver(post_delete, sender=Product)
def clear_product_cache_on_delete(sender, instance, **kwargs):
    print("Clear prod cache")
    cache.delete('product_list')

@receiver(post_save, sender=ProductVariant)
def clear_product_cache_on_save(sender, instance, **kwargs):
    print("Clear prod var cache") 
    cache.delete('product_variant_list')
    cache.delete('filters')

# Invalidate cache when a product is deleted
@receiver(post_delete, sender=ProductVariant)
def clear_product_cache_on_delete(sender, instance, **kwargs):
    print("Clear prod var cache") 
    cache.delete('product_variant_list')

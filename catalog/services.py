from django.core.cache import cache

from config.settings import CACHE_ENABLED
from .models import Product


def get_products_list_from_cache(category_id):
    """Получает данные по продуктам из кеша, если кеш пуст, получает данные из бд"""
    if not CACHE_ENABLED:
        return Product.objects.filter(category=category_id)
    key = f'products_list_category_{category_id}'
    products = cache.get(key)
    if products is not None:
        return products
    products = Product.objects.filter(category=category_id)
    cache.set(key, products)
    return products

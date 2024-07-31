from inventory.models import Product


def reduce_product_quantity(product_variant, quantity):
    product_variant.inventory -= quantity
    product_variant.save()

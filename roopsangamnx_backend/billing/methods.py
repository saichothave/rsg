from inventory.models import Product


def reduce_product_quantity(product, quantity):
    product.inventory -= quantity
    product.save()

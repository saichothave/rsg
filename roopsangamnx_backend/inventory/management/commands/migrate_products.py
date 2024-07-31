import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from inventory.models import Product, ProductVariant, ProductSize, ProductColor  # Update `your_app` with your actual app name

class Command(BaseCommand):
    help = 'Migrate existing products to new structure with ProductVariant'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        products = Product.objects.all()

        for product in products:
            variant = ProductVariant(
                product=product,
                size=product.size,
                color=product.color,
                mfd_date=datetime.date.today(),  # Placeholder for manufacturing date
                buying_price=product.buying_price,
                selling_price=product.selling_price,
                applicable_gst=product.applicable_gst,
                inventory=product.inventory
            )
            variant.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully migrated {products.count()} products.'))

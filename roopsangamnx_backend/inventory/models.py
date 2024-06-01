from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    hsn_code = models.CharField(max_length=20, unique=True, null=True, blank=True)
    qr_code = models.CharField(max_length=20, unique=True, null=True, blank=True)
    barcode = models.CharField(max_length=100, unique=True, null=True, blank=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    unit_buying_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit_selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    applicable_gst = models.DecimalField(max_digits=4, decimal_places=2)  # Updated to max_digits=4 to accommodate 100.00%
    quantity = models.IntegerField()

    def __str__(self):
        return self.name

from django.db import models

from roopsangamnx_backend.models import TimeStampedModel


class Category(TimeStampedModel):
    name = models.CharField(max_length=255, default="No category")

    def __str__(self):
        return self.name

class SubCategory(TimeStampedModel):
    name = models.CharField(max_length=255, default="No sub-category")
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Brand(TimeStampedModel):
    name = models.CharField(max_length=45, default="Local")
    def __str__(self):
        return self.name

class ProductColor(TimeStampedModel):
    color = models.CharField(max_length=45, default="No Color")
    inventory = models.IntegerField(default=0)
    def __str__(self):
        return self.color

class ProductSize(TimeStampedModel):
    size = models.CharField(max_length=10, default="Free Size")
    inventory = models.IntegerField(default=0)
    def __str__(self):
        return self.size

class Product(TimeStampedModel):
    name = models.CharField(max_length=255)
    brand = models.ForeignKey(Brand, related_name="models", on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='gallery/products', blank=True, null=True)
    size = models.ForeignKey(ProductSize, on_delete=models.CASCADE, blank=True, null=True)
    color = models.ForeignKey(ProductColor, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, blank=True, null=True, related_name='products')
    buying_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    applicable_gst = models.DecimalField(max_digits=4, decimal_places=2)  # Updated to max_digits=4 to accommodate 100.00%
    inventory = models.IntegerField(default=0)
    hsn_code = models.CharField(max_length=20, null=True, blank=True)
    qr_code = models.CharField(max_length=20, unique=True, null=True, blank=True)
    barcode = models.CharField(max_length=100, unique=True, null=True, blank=True)
    

    def __str__(self):
        return str(self.id)

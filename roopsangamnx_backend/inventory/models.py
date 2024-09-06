from django.db import models

from roopsangamnx_backend.models import TimeStampedModel
from django.core.exceptions import ValidationError


class Section(TimeStampedModel):

    class Meta:
        verbose_name = "Section"
        verbose_name_plural = "Sections"
        
    name = models.CharField(max_length=255, default="General", null=True, blank=True)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(TimeStampedModel):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=255, default="No category")
    section = models.ForeignKey(Section, related_name="categories", on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class SubCategory(TimeStampedModel):
    class Meta:
        verbose_name = "SubCategory"
        verbose_name_plural = "SubCategories"

    name = models.CharField(max_length=255, default="No sub-category")
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Brand(TimeStampedModel):
    name = models.CharField(max_length=45, default="Local")
    
    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
class ProductColor(TimeStampedModel):
    color = models.CharField(max_length=45, default="No Color")

    def save(self, *args, **kwargs):
        self.color = self.color.title()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id) + " " + str(self.color)

class ProductSize(TimeStampedModel):
    size = models.CharField(max_length=10, default="Free Size")

    def save(self, *args, **kwargs):
        self.size = self.size.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.size
    
class ProductArticle(TimeStampedModel):
    article = models.CharField(max_length=15)

    def __str__(self):
        return self.article

class Product(TimeStampedModel):
    name = models.CharField(max_length=255)
    brand = models.ForeignKey(Brand, related_name="models", on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='gallery/products', blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, blank=True, null=True, related_name='products')
    barcode = models.CharField(max_length=100, unique=True, null=True, blank=True, db_index=True)
    is_multi_pack = models.BooleanField(default=False)
    multi_pack_quantity = models.IntegerField(default=1)
    article_no = models.ForeignKey(ProductArticle, related_name='products', blank=True, null=True, on_delete=models.SET_NULL)

    # qr_code = models.CharField(max_length=20, null=True, blank=True)
    # size = models.ForeignKey(ProductSize, on_delete=models.SET_NULL, blank=True, null=True)
    # color = models.ForeignKey(ProductColor, on_delete=models.SET_NULL, blank=True, null=True)
    # buying_price = models.DecimalField(max_digits=10, decimal_places=2)
    # selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    # hsn_code = models.CharField(max_length=20, null=True, blank=True)
    # inventory = models.IntegerField(default=0)
    # applicable_gst = models.DecimalField(max_digits=4, decimal_places=2)  # Updated to max_digits=4 to accommodate 100.00%

    
    def save(self, *args, **kwargs):
        # Capitalize the first letter of each word in the size field
        self.name = self.name.title()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.section.name) + "/" +str(self.category) + "/" + str(self.subcategory)  + "/" + str(self.name)

class ProductVariant(TimeStampedModel):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    size = models.ForeignKey(ProductSize, on_delete=models.CASCADE, blank=True, null=True)
    color = models.ForeignKey(ProductColor, on_delete=models.CASCADE, blank=True, null=True)
    mfd_date = models.DateField()
    buying_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    applicable_gst = models.DecimalField(max_digits=4, decimal_places=2)
    inventory = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Product Variant"
        verbose_name_plural = "Product Variants"
        ordering = ['product', 'mfd_date']

    def save(self, *args, **kwargs):
        if self.buying_price > self.selling_price:
            raise ValidationError("Selling price cannot be less than buying price")
        super().save(*args, **kwargs)

    def clean(self):
        # Check for duplicate product variants
        if ProductVariant.objects.filter(
            product__name=self.product.name,
            product__brand=self.product.brand,
            product__section=self.product.section,
            product__category=self.product.category,
            product__subcategory=self.product.subcategory,
            product__barcode=self.product.barcode,
            mfd_date=self.mfd_date,
            color=self.color,
            size=self.size
        ).exclude(id=self.id).exists():
            raise ValidationError("Product variant with the same details already exists.")


    def __str__(self):
        return f"{self.product.name} - {self.mfd_date}"


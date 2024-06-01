from django.db import models
from inventory.models import Product


class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name


class BillingDesk(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Billing(models.Model):
    billing_desk = models.ForeignKey(BillingDesk, on_delete=models.CASCADE, related_name='billings')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='billings')
    date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    gst_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=255)

    def __str__(self):
        return f"Billing #{self.id} - {self.customer.name}"


class BillingItem(models.Model):
    billing = models.ForeignKey(Billing, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=3, decimal_places=2)


    def __str__(self):
        return f"{self.product.name} - {self.quantity} pcs"


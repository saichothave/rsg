from django.db import models
from inventory.models import Product
from authentication.models import BillingDesk
from roopsangamnx_backend.models import TimeStampedModel


class Customer(TimeStampedModel):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name



class Billing(TimeStampedModel):
    billing_desk = models.ForeignKey(BillingDesk, on_delete=models.CASCADE, related_name='billings')
    customer_details = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='billings')
    date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    gst_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    transaction_id = models.CharField(max_length=255)
    isPaid = models.BooleanField(default=False)
    payment_mode = models.CharField(max_length=30, default="Cash")

    def __str__(self):
        return f"Billing #{self.id} - {self.customer_details.name}"


class BillingItem(TimeStampedModel):
    billing = models.ForeignKey(Billing, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=6, decimal_places=2)


    def __str__(self):
        return f"{self.product.name} - {self.quantity} pcs"


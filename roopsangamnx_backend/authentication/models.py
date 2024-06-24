from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.

class RSGUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('shopowner', 'ShopOwner'),
        ('billingdesk', 'BillingDesk'),
        ('scanner', 'Scanner'),
    )
    user_type = models.CharField(max_length=50, choices=USER_TYPE_CHOICES)
    
    # Add related_name arguments to avoid clashes
    groups = models.ManyToManyField(
        Group,
        related_name='rsguser_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='rsguser',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='rsguser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='rsguser',
    )

class ShopOwner(models.Model):
    user = models.OneToOneField(RSGUser, on_delete=models.CASCADE, primary_key=True)
    shop_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

class BillingDesk(models.Model):
    user = models.OneToOneField(RSGUser, on_delete=models.CASCADE, primary_key=True)
    location = models.CharField(max_length=255)
    assigned_shop = models.ForeignKey(ShopOwner, on_delete=models.CASCADE)

class Scanner(models.Model):
    user = models.OneToOneField(RSGUser, on_delete=models.CASCADE, primary_key=True)
    assigned_desk = models.ForeignKey(BillingDesk, on_delete=models.CASCADE)

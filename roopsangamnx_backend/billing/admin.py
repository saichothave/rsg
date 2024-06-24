from django.contrib import admin
from .models import Customer, Billing, BillingItem

admin.site.register(Customer)
admin.site.register(Billing)
admin.site.register(BillingItem)

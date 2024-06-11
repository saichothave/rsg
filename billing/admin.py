from django.contrib import admin
from .models import Customer, Billing, BillingDesk, BillingItem

admin.site.register(Customer)
admin.site.register(Billing)
admin.site.register(BillingDesk)
admin.site.register(BillingItem)

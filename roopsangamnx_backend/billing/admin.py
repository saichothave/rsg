from django.contrib import admin
from .models import Customer, Billing, BillingItem


class BillingAdmin(admin.ModelAdmin):
    model = Billing
    list_display = [
        'id','customer_details', 'total_amount', 'date', 'payment_mode'
    ]
    search_fields = [ 'id','customer_details__name','total_amount', 'date']

class BillingItemAdmin(admin.ModelAdmin):
    model = BillingItem
    list_display = [
        'billing', 'product', 'unit_price', 'quantity', 'discount',  'total_price'
    ]
    search_fields = [ 'product__name','product__barcode']



admin.site.register(Customer)
admin.site.register(Billing, BillingAdmin)
admin.site.register(BillingItem, BillingItemAdmin)

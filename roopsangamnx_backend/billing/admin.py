from django.contrib import admin
from .models import Customer, Billing, BillingItem
from unfold.admin import ModelAdmin


class BillingAdmin(ModelAdmin):
    model = Billing
    list_display = [
        'id','customer_details', 'total_amount', 'date', 'isPaid', 'payment_mode'
    ]
    search_fields = [ 'id','customer_details__name','total_amount', 'date']

class BillingItemAdmin(ModelAdmin):
    model = BillingItem
    list_display = [
        'billing', 'product', 'unit_price', 'quantity', 'discount',  'total_price', 
    ]
    search_fields = [ 'id','billing__id','product__name','product__barcode']



admin.site.register(Customer)
admin.site.register(Billing, BillingAdmin)
admin.site.register(BillingItem, BillingItemAdmin)

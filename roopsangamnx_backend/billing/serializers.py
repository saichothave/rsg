from rest_framework import serializers
from .models import Customer, BillingDesk, Billing, BillingItem
from inventory.serializers import ProductSerializer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'phone_number']


class BillingDeskSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingDesk
        fields = ['id', 'name', 'location']


class BillingSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    billing_desk = BillingDeskSerializer()
    items = serializers.SerializerMethodField()

    class Meta:
        model = Billing
        fields = ['id', 'billing_desk', 'customer', 'date', 'total_amount', 'gst_amount', 'grand_total', 'transaction_id', 'items']

    def get_items(self, obj):
        items = obj.items.all()
        return BillingItemSerializer(items, many=True).data


class BillingItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = BillingItem
        fields = ['id', 'product', 'quantity', 'unit_price', 'total_price', 'discount']

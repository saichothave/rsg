from django.db import transaction
from rest_framework import serializers
from authentication.serializers import BillingDeskSerializer
from inventory.models import Product
from .models import Customer, BillingDesk, Billing, BillingItem
from inventory.serializers import ProductSerializer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'phone_number']


class BillingItemSerializer(serializers.ModelSerializer):
    # product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())  # Use PrimaryKeyRelatedField for product
    product = ProductSerializer(read_only=True)  # Include product details in response
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True, source='product')


    class Meta:
        model = BillingItem
        fields = ['product', 'product_id', 'quantity', 'unit_price', 'total_price', 'discount']


class BillingSerializer(serializers.ModelSerializer):
    items = BillingItemSerializer(many=True)
    customer_details = CustomerSerializer()
    billing_desk = BillingDeskSerializer(read_only=True)  # Include BillingDesk details in response
    billing_desk_id = serializers.PrimaryKeyRelatedField(queryset=BillingDesk.objects.all(), write_only=True, source='billing_desk')
    # billing_desk = serializers.PrimaryKeyRelatedField(queryset=BillingDesk.objects.all())

    class Meta:
        model = Billing
        fields = ['billing_desk', 'billing_desk_id', 'customer_details', 'date', 'total_amount', 'gst_amount', 'transaction_id', 'isPaid', 'payment_mode', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        customer_data = validated_data.pop('customer_details')

        # Create or get the customer instance
        customer_instance = None
        if(customer_data['email']):
            customer_instance, created = Customer.objects.get_or_create(email=customer_data['email'], defaults=customer_data)
        else:
            customer_instance = Customer()
            customer_instance.name = customer_data['name']
            customer_instance.email = customer_data['email']
            customer_instance.phone_number = customer_data['phone_number']
            customer_instance.save()
        print(customer_instance)

        billing = Billing.objects.create(customer_details=customer_instance,**validated_data)

        for item_data in items_data:
            product_id = item_data.get('product').id
            if not Product.objects.filter(id=product_id).exists():
                raise serializers.ValidationError({'product': f'Product with id {product_id} does not exist.'})

            BillingItem.objects.create(billing=billing, **item_data)
        return billing
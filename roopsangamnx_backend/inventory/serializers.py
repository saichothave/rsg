from rest_framework import serializers
from .models import Category, Product, SubCategory

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubcategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer()  # Nested category

    class Meta:
        model = SubCategory
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    subcategory = SubcategorySerializer()

    class Meta:
        model = Product
        fields = ['id', 'name', 'brand', 'hsn_code', 'qr_code', 'barcode', 'description', 'category', 'subcategory', 'unit_buying_price', 'unit_selling_price', 'applicable_gst', 'quantity']

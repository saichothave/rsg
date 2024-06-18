from rest_framework import serializers
from .models import Category, Product, SubCategory, Brand, ProductColor, ProductSize


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'category']

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'subcategories']
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name']


class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ['id', 'color', 'inventory']

class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = ['id', 'size', 'inventory']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    subcategory = SubcategorySerializer()
    brand = BrandSerializer()
    size = ProductSizeSerializer()
    color = ProductColorSerializer()
    class Meta:
        model = Product
        fields = ['id', 'name', 'brand', 'image', 'size', 'color', 'description', 'category', 'subcategory', 'buying_price', 'selling_price', 'applicable_gst', 'inventory', 'hsn_code', 'qr_code', 'barcode']
        depth=1
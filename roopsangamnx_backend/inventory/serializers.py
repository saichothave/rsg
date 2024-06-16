from rest_framework import serializers
from .models import Category, Product, SubCategory, Brand, ProductColor, ProductSize

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubcategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer()  # Nested category

    class Meta:
        model = SubCategory
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = '__all__'

class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    subcategory = SubcategorySerializer()
    brand = BrandSerializer()
    size = ProductSizeSerializer()
    color = ProductColorSerializer()
    class Meta:
        model = Product
        fields = '__all__'
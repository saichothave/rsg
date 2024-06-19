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

    # def create(self, validated_data):
    #     return Product.objects.create(**validated_data)

    # def create(self, validated_data):
    #     print("From Serl")
    #     brand_data = validated_data.pop('brand')
    #     category_data = validated_data.pop('category')
    #     subcategory_data = validated_data.pop('subcategory', None)
    #     size_data = validated_data.pop('size', None)
    #     color_data = validated_data.pop('color', None)

    #     brand, created = Brand.objects.get_or_create(name=brand_data['name'])
    #     category, created = Category.objects.get_or_create(name=category_data['name'])
        
    #     subcategory = None
    #     if subcategory_data:
    #         subcategory, created = SubCategory.objects.get_or_create(
    #             name=subcategory_data['name'],
    #             defaults={'category': category}
    #         )

    #     size = None
    #     if size_data:
    #         size, created = ProductSize.objects.get_or_create(size=size_data['size'])

    #     color = None
    #     if color_data:
    #         color, created = ProductColor.objects.get_or_create(color=color_data['color'])

    #     print("OKOKOK")

    #     product = Product.objects.create(
    #         brand=brand,
    #         category=category,
    #         subcategory=subcategory,
    #         size=size,
    #         color=color,
    #         **validated_data
    #     )
    #     return product
    
    # # def create(self, validated_data):
    #     brand_data = validated_data.pop('brand')
    #     category_data = validated_data.pop('category')
    #     subcategory_data = validated_data.pop('subcategory')
    #     size_data = validated_data.pop('size')
    #     color_data = validated_data.pop('color')

    #     brand = Brand.objects.create(**brand_data)
    #     category = Category.objects.create(**category_data)
    #     subcategory = Subcategory.objects.create(**subcategory_data)
    #     size = Size.objects.create(**size_data)
    #     color = Color.objects.create(**color_data)

    #     product = Product.objects.create(
    #         brand=brand,
    #         category=category,
    #         subcategory=subcategory,
    #         size=size,
    #         color=color,
    #         **validated_data
    #     )

    #     return product

    
class ProductWriteSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    subcategory = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all(), required=False, allow_null=True)
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())
    size = serializers.PrimaryKeyRelatedField(queryset=ProductSize.objects.all(), required=False, allow_null=True)
    color = serializers.PrimaryKeyRelatedField(queryset=ProductColor.objects.all(), required=False, allow_null=True)
    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        return Product.objects.create(**validated_data) 
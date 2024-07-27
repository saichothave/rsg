from rest_framework import serializers
from .models import Category, Product, ProductArticle, Section, SubCategory, Brand, ProductColor, ProductSize



class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = "__all__"

class SectionSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = "__all__"

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = "__all__"

class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = "__all__"

class ProductArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductArticle
        fields = "__all__"  

class ProductSerializer(serializers.ModelSerializer):
    section = SectionSerializer()
    category = CategorySerializer()
    subcategory = SubcategorySerializer()
    brand = BrandSerializer()
    size = ProductSizeSerializer()
    color = ProductColorSerializer()
    article_no = ProductArticleSerializer() 
    
    class Meta:
        model = Product
        fields = '__all__'
        depth=1
    
    # def create(self, validated_data):
        
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
    section = serializers.PrimaryKeyRelatedField(queryset=Section.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    subcategory = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all(), required=False, allow_null=True)
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())
    size = serializers.PrimaryKeyRelatedField(queryset=ProductSize.objects.all(), required=False, allow_null=True)
    color = serializers.PrimaryKeyRelatedField(queryset=ProductColor.objects.all())
    article_no = serializers.PrimaryKeyRelatedField(queryset=ProductArticle.objects.all(), required=False, allow_null=True)
    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        return Product.objects.create(**validated_data) 

    def update(self, instance, validated_data):
        instance.section = validated_data.get('section', instance.section)
        instance.category = validated_data.get('category', instance.category)
        instance.subcategory = validated_data.get('subcategory', instance.subcategory)
        instance.brand = validated_data.get('brand', instance.brand)
        instance.size = validated_data.get('size', instance.size)
        instance.color = validated_data.get('color', instance.color)
        instance.article_no = validated_data.get('article_no', instance.article_no)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
    

class FilterSerializer(serializers.Serializer):
    section = SectionSerializer(many=True)
    categories = CategorySerializer(many=True)
    subcategories = SubcategorySerializer(many=True)
    brands = BrandSerializer(many=True)
    product_colors = ProductColorSerializer(many=True)
    product_sizes = ProductSizeSerializer(many=True)
    product_article = ProductArticleSerializer(many=True)
    

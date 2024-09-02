from rest_framework import serializers
from .models import Category, Product, ProductArticle, ProductVariant, Section, SubCategory, Brand, ProductColor, ProductSize



class SectionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, required=False, allow_blank=True)

    class Meta:
        model = Section
        fields = ('id', 'name')


class CategorySerializer(serializers.ModelSerializer):
    # subcategories = SubcategorySerializer(many=True, read_only=True)
    name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    section = SectionSerializer()
    class Meta:
        model = Category
        fields = ('id', 'name', 'section')


class SubcategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    category = CategorySerializer()
    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'category')

class BrandSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    class Meta:
        model = Brand
        fields = ('id', 'name')


class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ('id', 'color')

class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = ('id', 'size')

class ProductArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductArticle
        fields = ('id', 'article') 


class ProductVariantSerializer(serializers.ModelSerializer):
    size = ProductSizeSerializer()
    color = ProductColorSerializer()

    class Meta:
        model = ProductVariant
        fields = ['id', 'size', 'color', 'mfd_date', 'buying_price', 'selling_price', 'applicable_gst', 'inventory']


class ProductSerializer(serializers.ModelSerializer):
    section = SectionSerializer()
    category = CategorySerializer()
    subcategory = SubcategorySerializer()
    brand = BrandSerializer()
    article_no = ProductArticleSerializer()
    variants = ProductVariantSerializer(many=True)
    
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
    

# unused
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


# class NewProductSerializer(serializers.ModelSerializer):
#     variants = ProductVariantSerializer(many=True)
#     section = SectionSerializer()
#     category = CategorySerializer()
#     subcategory = SubcategorySerializer()
#     brand = BrandSerializer()
#     article_no = ProductArticleSerializer()

#     class Meta:
#         model = Product
#         fields = '__all__'

#     def create_or_get(self, model, validated_data):
#         instance, created = model.objects.get_or_create(**validated_data)
#         return instance

#     def create(self, validated_data):
#         variants_data = validated_data.pop('variants')
        
#         section_data = validated_data.pop('section')
#         section = self.create_or_get(Section, section_data)
        
#         category_data = validated_data.pop('category')
#         category = self.create_or_get(Category, category_data)
        
#         subcategory_data = validated_data.pop('subcategory')
#         subcategory = self.create_or_get(SubCategory, subcategory_data)
        
#         brand_data = validated_data.pop('brand')
#         brand = self.create_or_get(Brand, brand_data)
        
#         article_no_data = validated_data.pop('article_no')
#         article_no = self.create_or_get(ProductArticle, article_no_data)
        
#         product = Product.objects.create(
#             section=section,
#             category=category,
#             subcategory=subcategory,
#             brand=brand,
#             article_no=article_no,
#             **validated_data
#         )
        
#         for variant_data in variants_data:
#             size_data = variant_data.pop('size')
#             size = self.create_or_get(ProductSize, size_data)
            
#             color_data = variant_data.pop('color')
#             color = self.create_or_get(ProductColor, color_data)
            
#             ProductVariant.objects.create(product=product, size=size, color=color, **variant_data)
        
#         return product
    
    
class NewProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True)
    section = SectionSerializer()
    category = CategorySerializer()
    subcategory = SubcategorySerializer()
    brand = BrandSerializer()
    article_no = ProductArticleSerializer()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'brand', 'image', 'description', 'section', 'category', 'subcategory', 'barcode',
            'is_multi_pack', 'multi_pack_quantity', 'article_no', 'created_at', 'updated_at', 'variants'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create_or_get(self, model, validated_data):
        data = model.objects.filter(**validated_data).first()
        if not data:
            instance, created = model.objects.get_or_create(**validated_data)
            return instance
        else:
            return data

    def create(self, validated_data):
        variants_data = validated_data.pop('variants')
        
        section_data = validated_data.pop('section')
        section = self.create_or_get(Section, section_data)
        
        category_data = validated_data.pop('category')
        category_data['section'] = section
        category = self.create_or_get(Category, category_data)
        
        subcategory_data = validated_data.pop('subcategory')
        subcategory_data['category'] = category
        subcategory = self.create_or_get(SubCategory, subcategory_data)
        
        brand_data = validated_data.pop('brand')
        brand = self.create_or_get(Brand, brand_data)
        
        article_no_data = validated_data.pop('article_no')
        article_no = self.create_or_get(ProductArticle, article_no_data)
        
        product = Product.objects.create(
            section=section,
            category=category,
            subcategory=subcategory,
            brand=brand,
            article_no=article_no,
            **validated_data
        )
        
        for variant_data in variants_data:
            size_data = variant_data.pop('size')
            size = self.create_or_get(ProductSize, size_data)
            
            color_data = variant_data.pop('color')
            color = self.create_or_get(ProductColor, color_data)
            
            ProductVariant.objects.create(product=product, size=size, color=color, **variant_data)
        
        return product
    

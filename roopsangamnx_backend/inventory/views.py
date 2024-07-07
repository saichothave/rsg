from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from inventory.filters import CategoryFilter, SubCategoryFilter, ProductFilter, SectionFilter
from .models import Category, Product, SubCategory, Brand, ProductColor, ProductSize
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView

from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
import json


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated] 
    filter_backends = [DjangoFilterBackend]
    filterset_class = SectionFilter

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated] 
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter

class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubcategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = SubCategoryFilter

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    parser_classes = (JSONParser, MultiPartParser, FormParser)

    def get_queryset(self):
        products = Product.objects.all().order_by('-updated_at')
        return products

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return ProductWriteSerializer  # Use WriteSerializer for POST requests
        return self.serializer_class  # Use ReadSerializer for other operations

    def create(self, request, *args, **kwargs):
        data = request.data
        _mutable = data._mutable

        # set to mutable
        data._mutable = True
        # Ensure nested JSON fields are parsed correctly
        for field in ['brand', 'section', 'category', 'subcategory', 'size', 'color']:
            if field in data and isinstance(data[field], str):
                try:
                    data[field] = json.loads(data[field])
                except json.JSONDecodeError:
                    return Response({'error': f'Invalid JSON format for {field}'}, status=status.HTTP_400_BAD_REQUEST)

        # Extract and create or retrieve related objects
        brand = self.get_or_create_brand(data.get('brand'))
        section = self.get_or_create_section(data.get('section'))
        category = self.get_or_create_category(data.get('category'), section)
        subcategory = self.get_or_create_subcategory(data.get('subcategory'), category)
        size = self.get_or_create_product_size(data.get('size'))
        color = self.get_or_create_product_color(data.get('color'))

        # Assign the primary keys of related objects to data dictionary
        data['brand'] = brand.pk
        data['section'] = section.pk
        data['category'] = category.pk

        if subcategory:
            data['subcategory'] = subcategory.pk
        if size:
            data['size'] = size.pk
        if color:
            data['color'] = color.pk

        # Validate and save the serializer
        # set mutable flag back
        data._mutable = _mutable
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        data._mutable = True

        data['brand'] = brand
        data['section'] = section
        data['category'] = category

        if subcategory:
            data['subcategory'] = subcategory
        if size:
            data['size'] = size
        if color:
            data['color'] = color

        # Validate and save the serializer
        # set mutable flag back
        data._mutable = _mutable

        # Return the response
        headers = self.get_success_headers(serializer.data)
        return Response(ProductSerializer(data).data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        data = request.data
        _mutable = data._mutable

        # set to mutable
        data._mutable = True
        # Ensure nested JSON fields are parsed correctly
        for field in ['brand', 'section', 'category', 'subcategory', 'size', 'color']:
            if field in data and isinstance(data[field], str):
                try:
                    data[field] = json.loads(data[field])
                except json.JSONDecodeError:
                    return Response({'error': f'Invalid JSON format for {field}'}, status=status.HTTP_400_BAD_REQUEST)

        # Extract and create or retrieve related objects
        brand = self.get_or_create_brand(data.get('brand'))
        section = self.get_or_create_section(data.get('section'))
        category = self.get_or_create_category(data.get('category'), section)
        subcategory = self.get_or_create_subcategory(data.get('subcategory'), category)
        size = self.get_or_create_product_size(data.get('size'))
        color = self.get_or_create_product_color(data.get('color'))

        # Assign the primary keys of related objects to data dictionary
        data['brand'] = brand.pk
        data['section'] = section.pk
        data['category'] = category.pk
        
        if subcategory:
            data['subcategory'] = subcategory.pk
        if size:
            data['size'] = size.pk
        if color:
            data['color'] = color.pk

        # Validate and save the serializer
        # set mutable flag back
        data._mutable = _mutable
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


    def get_or_create_brand(self, brand_data):
        if not brand_data:
            return None

        brand_name = brand_data.get('name').title()

        try:
            brand = Brand.objects.get(name__iexact=brand_name) 
        except:
            brand, created = Brand.objects.get_or_create(name=brand_name)
        return brand
    
    def get_or_create_section(self, section_data):
        if not section_data:
            return None

        section_name = section_data.get('name').title()
        try:
            section = Section.objects.get(name__iexact=section_name) 
        except:
            section, created = Section.objects.get_or_create(name=section_name)
        return section

    def get_or_create_category(self, category_data, section):
        if not category_data:
            return None

        category_name = category_data.get('name')
        try:
            category = Category.objects.get(name__iexact=category_name) 
        except:
            category, created = Category.objects.get_or_create(name=category_name, section=section)
        return category

    def get_or_create_subcategory(self, subcategory_data, category):
        if not subcategory_data:
            return None

        subcategory_name = subcategory_data.get('name')
        try:
            subcategory = SubCategory.objects.get(name__iexact=subcategory_name) 
        except:
            subcategory, created = SubCategory.objects.get_or_create(name=subcategory_name, category=category)

        return subcategory

    def get_or_create_product_size(self, size_data):
        if not size_data:
            return None

        size_name = size_data.get('size')
        try:
            size = ProductSize.objects.get(size__iexact=size_name)
        except:
            size, created = ProductSize.objects.get_or_create(size=size_name)
        return size

    def get_or_create_product_color(self, color_data):
        if not color_data:
            return None

        color_name = color_data.get('color').title()
        try:
            color = ProductColor.objects.get(color__iexact=color_name)
        except:
            color, created = ProductColor.objects.get_or_create(color=color_name)
        return color

class FilterView(APIView):
    def get(self, request, *args, **kwargs):
        sections = Section.objects.all()
        categories = Category.objects.all()
        subcategories = SubCategory.objects.all()
        brands = Brand.objects.all()
        product_colors = ProductColor.objects.all()
        product_sizes = ProductSize.objects.all()
        
        data = {
            'sections': SectionSerializer(sections, many=True).data,
            'categories': CategorySerializer(categories, many=True).data,
            'subcategories': SubcategorySerializer(subcategories, many=True).data,
            'brands': BrandSerializer(brands, many=True).data,
            'product_colors': ProductColorSerializer(product_colors, many=True).data,
            'product_sizes': ProductSizeSerializer(product_sizes, many=True).data,
        }
        
        return Response(data)
   
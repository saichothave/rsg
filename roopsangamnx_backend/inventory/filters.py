import django_filters
from .models import Category, SubCategory, Product

class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Category
        fields = ['name']

class SubCategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.NumberFilter(field_name='category__id')

    class Meta:
        model = SubCategory
        fields = ['name', 'category']

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    brand = django_filters.NumberFilter(field_name='brand__id')
    category = django_filters.NumberFilter(field_name='category__id')
    subcategory = django_filters.NumberFilter(field_name='subcategory__id')
    min_price = django_filters.NumberFilter(field_name='selling_price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='selling_price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['name', 'brand', 'category', 'subcategory', 'min_price', 'max_price']


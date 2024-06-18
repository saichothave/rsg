from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from inventory.filters import CategoryFilter, SubCategoryFilter, ProductFilter
from .models import Category, Product, SubCategory
from .serializers import CategorySerializer, ProductSerializer, SubcategorySerializer
from django_filters.rest_framework import DjangoFilterBackend



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
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

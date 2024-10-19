from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, InsertProductRow, ProductByBarcodeAPIView, ProductInventoryByCategory, ProductVariantImportView, ProductViewSet, SubcategoryViewSet, FilterView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'subcategories', SubcategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('filters/', FilterView.as_view(), name='filters'),
    path('products/barcode/<str:barcode>/', ProductByBarcodeAPIView.as_view(), name='product-by-barcode'),
    path('product-inventory-by-category/', ProductInventoryByCategory.as_view(), name='product-inventory-by-category'),
    path('import-products/', ProductVariantImportView.as_view(), name='import-products'),
    path('insert-product/', InsertProductRow.as_view(), name='insert-products'),

]

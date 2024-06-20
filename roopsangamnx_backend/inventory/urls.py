from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, SubcategoryViewSet, FilterView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'subcategories', SubcategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('filters/', FilterView.as_view(), name='filters')
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomerViewSet,
    BillingViewSet, BillingItemViewSet
)

# Create a router object
router = DefaultRouter()

# Register viewsets with the router
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'billings', BillingViewSet, basename='billing')
router.register(r'billing-items', BillingItemViewSet, basename='billing-item')

# Define the URL patterns
urlpatterns = [
    path('', include(router.urls)),
]

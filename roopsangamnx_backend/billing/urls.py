from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BDDashBoardView,
    CustomerViewSet,
    BillingViewSet, BillingItemViewSet,
    DailySalesChartView,
    GetBills,
    GetCustomerByPhoneNumber,
    PrinterStatus,
    PrintInvoiceByNumber
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
    path('todays-total-by-payment-mode/', BDDashBoardView.as_view(), name='todays-total-by-payment-mode'),
    path('customer-by-phone/<str:phone_number>/', GetCustomerByPhoneNumber.as_view(), name='customer-by-phone'),
    path('printer-status/', PrinterStatus.as_view(), name='printer-status'),
    path('print-bill/<str:invoice_number>/', PrintInvoiceByNumber.as_view(), name='print-bill'),
    path('get-bills/', GetBills.as_view(), name='get-bill'),
    path('daily-sales/', DailySalesChartView.as_view(), name='daily-sales'),

]

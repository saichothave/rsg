from rest_framework import viewsets
from .models import Customer, BillingDesk, Billing, BillingItem
from .serializers import CustomerSerializer, BillingDeskSerializer, BillingSerializer, BillingItemSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class BillingDeskViewSet(viewsets.ModelViewSet):
    queryset = BillingDesk.objects.all()
    serializer_class = BillingDeskSerializer

class BillingViewSet(viewsets.ModelViewSet):
    queryset = Billing.objects.all()
    serializer_class = BillingSerializer

class BillingItemViewSet(viewsets.ModelViewSet):
    queryset = BillingItem.objects.all()
    serializer_class = BillingItemSerializer

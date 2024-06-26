from rest_framework import viewsets
from authentication.permissions import IsShopOwner, IsBillingDesk
from .invoice import generate_invoice_image
from .models import Customer, BillingDesk, Billing, BillingItem
from .serializers import CustomerSerializer, BillingDeskSerializer, BillingSerializer, BillingItemSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from rest_framework import status
from rest_framework import generics, permissions



class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class BillingViewSet(viewsets.ModelViewSet):
    queryset = Billing.objects.all()
    serializer_class = BillingSerializer
    permission_classes = [permissions.IsAuthenticated, IsBillingDesk]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data
        data["billing_desk_id"] = request.user.pk
        print(request.user)
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            invoice = serializer.save()
            response = generate_invoice_image(invoice, request)
            return response
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class BillingItemViewSet(viewsets.ModelViewSet):
    queryset = BillingItem.objects.all()
    serializer_class = BillingItemSerializer

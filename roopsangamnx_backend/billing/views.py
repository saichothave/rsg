from django.db.models import Sum
from rest_framework import viewsets
from authentication.permissions import IsShopOwner, IsBillingDesk
from .invoice import generate_invoice_image
from .models import Customer, BillingDesk, Billing, BillingItem
from .serializers import BDDashBoardSerializer, BillingListSerializer, CustomerSerializer, BillingDeskSerializer, BillingSerializer, BillingItemSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from rest_framework import status
from rest_framework import generics, permissions

from django.utils import timezone
from .printer import p
from billing import printer




class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class BillingViewSet(viewsets.ModelViewSet):
    queryset = Billing.objects.all()
    serializer_class = BillingSerializer
    permission_classes = [permissions.IsAuthenticated, IsBillingDesk]


    def get_serializer_class(self):
        if self.action == 'list':
            return BillingListSerializer
        return BillingSerializer
    
    def get_queryset(self):
        return self.queryset.select_related('customer_details')

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
        else:
            print("not valid", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class BillingItemViewSet(viewsets.ModelViewSet):
    queryset = BillingItem.objects.all()
    serializer_class = BillingItemSerializer

class BDDashBoardView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsBillingDesk]

    def get(self, request, *args, **kwargs):
        today = timezone.now().date()
        today_bills = Billing.objects.filter(date__date=today, isPaid=True)
        total_by_payment_mode = today_bills.values('payment_mode').annotate(total_amount=Sum('total_amount'))
        
        serializer = BDDashBoardSerializer(total_by_payment_mode, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class GetCustomerByPhoneNumber(APIView):
    def get(self, request, phone_number):
        try:
            customer = Customer.objects.filter(phone_number__icontains=phone_number)
            serializer = CustomerSerializer(customer, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
        

class PrinterStatus(APIView):
    def get(self, request):
        print('printer status')
        print('p', p.device)
        if p.device and p.is_online:
            p.buzzer(1)
            return Response({'success': 'Printer is Connected'}, status=status.HTTP_200_OK)
        else:
            k = printer.initialize_printer()
            if k.is_online:
                k.buzzer(1)
                return Response({'success': 'Printer is Connected'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Customer not found'}, status=status.HTTP_226_IM_USED)
            
class PrintInvoiceByNumber(APIView):
    def get(self, request, invoice_number):
        try:
            invoice = Billing.objects.get(pk=invoice_number)
            print(invoice)
            response = generate_invoice_image(invoice, request)
            return response
            # return Response(serializer.data, status=status.HTTP_200_OK)
        except Billing.DoesNotExist:
            return Response({'error': 'Invoice not found'}, status=status.HTTP_404_NOT_FOUND)
        


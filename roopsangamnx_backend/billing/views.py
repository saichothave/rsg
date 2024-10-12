from django.db.models import Sum
from rest_framework import viewsets
from authentication.permissions import IsAppUser, IsShopOwner, IsBillingDesk
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
from django.utils.timezone import now, timedelta, make_aware
from datetime import datetime
from django.db.models.functions import TruncDate





class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]


class BillingViewSet(viewsets.ModelViewSet):
    queryset = Billing.objects.all()
    serializer_class = BillingSerializer
    # permission_classes = [permissions.IsAuthenticated, IsAppUser]


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
            response = generate_invoice_image(invoice, request, False, False)
            return response
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("not valid", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class BillingItemViewSet(viewsets.ModelViewSet):
    queryset = BillingItem.objects.all()
    serializer_class = BillingItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsBillingDesk]

class BDDashBoardView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsBillingDesk]

    def get(self, request, *args, **kwargs):
        today = timezone.localtime(timezone.now()).date()
        today_bills = Billing.objects.filter(date__date=today, isPaid=True)
        total_by_payment_mode = today_bills.values('payment_mode').annotate(total_amount=Sum('total_amount'))
        
        serializer = BDDashBoardSerializer(total_by_payment_mode, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GetBills(APIView):
    permission_classes = [permissions.IsAuthenticated, IsBillingDesk]

    def get(self, request, *args, **kwargs):
        today = timezone.localtime(timezone.now()).date()
        today_bills = Billing.objects.filter(date__date=today, isPaid=True)
        serializer = BillingListSerializer(today_bills, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class GetCustomerByPhoneNumber(APIView):
    permission_classes = [IsAppUser] 

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
        return Response({'success': 'Printer is Connected'}, status=status.HTTP_200_OK) # Disabled Django printing functionality
        # if p.device and p.is_online:
        #     p.buzzer(1)
        #     return Response({'success': 'Printer is Connected'}, status=status.HTTP_200_OK)
        # else:
        #     k = printer.initialize_printer()
        #     if k.is_online:
        #         k.buzzer(1)
        #         return Response({'success': 'Printer is Connected'}, status=status.HTTP_200_OK)
        #     else:
        #         return Response({'error': 'Customer not found'}, status=status.HTTP_226_IM_USED)
            
class PrintInvoiceByNumber(APIView):
    permission_classes = [IsAppUser]

    def get(self, request, invoice_number):
        try:
            imageOnly = request.query_params.get('imageOnly', 'false').lower() == 'true'
            print(imageOnly)
            invoice = Billing.objects.get(pk=invoice_number)
            response = generate_invoice_image(invoice, request, True, imageOnly)
            return response
            # return Response(serializer.data, status=status.HTTP_200_OK)
        except Billing.DoesNotExist:
            return Response({'error': 'Invoice not found'}, status=status.HTTP_404_NOT_FOUND)
        
class DailySalesChartView(APIView):
    def get(self, request, *args, **kwargs):
       # Get the date 100 days ago from the current time
        days_ago = timezone.localtime(timezone.now()) - timedelta(days=100)

        # Filter billings and group by day, summing the total_amount
        billings = Billing.objects.filter(date__gte=days_ago)

        daily_sales = (
            billings
            .annotate(day=TruncDate('date'))  # Truncate the datetime to just the date (day)
            .values('day')                    # Group by the day
            .annotate(total_sales=Sum('total_amount'))  # Sum the total_amount for each day
            .order_by('day')  # Sort by day
        )

    

        # Format the response for chart consumption
        labels = [datetime.strptime(str(entry['day']), "%Y-%m-%d").strftime("%d-%b") for entry in daily_sales]
        sales_data = [entry['total_sales'] for entry in daily_sales]

        return Response({
            "labels": labels,
            "sales_data": sales_data
        })
        


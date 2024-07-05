from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from roopsangamnx_backend import settings
from .serializers import RSGUserSerializer, LoginSerializer
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import generics, permissions
from django.contrib.auth import authenticate, login
from .models import RSGUser
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.views import APIView

from rest_framework import generics, permissions
from .serializers import ShopOwnerSerializer, BillingDeskSerializer, ScannerSerializer
from .models import ShopOwner, BillingDesk, Scanner
from .permissions import IsShopOwner, IsBillingDesk

class RSGUserCreate(generics.CreateAPIView):
    queryset = RSGUser.objects.all()
    serializer_class = RSGUserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save()
        RSGUser.objects.create(user=user)


class UnauthorizedException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Unauthorized'
    default_code = 'unauthorized'


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(generics.CreateAPIView):
    csrf_exempt = True
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    


    def post(self, request, *args, **kwargs):
        print('request')
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                try :
                    login(request, user)
                    token, created = Token.objects.get_or_create(user=user)
                    # request.session['token'] = token.key
                    response = Response({"token": token.key, "user": RSGUserSerializer(user).data }, status=200)
                    response.set_cookie('token', token.key, max_age=3600, httponly=True)
                    return response
                except RSGUser.DoesNotExist:
                    raise UnauthorizedException("Invalid credentials")
            else:
                raise UnauthorizedException("Invalid credentials")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
class ShopOwnerCreateView(generics.ListCreateAPIView):
    queryset = ShopOwner.objects.all()
    serializer_class = ShopOwnerSerializer
    permission_classes = [permissions.IsAdminUser]
    

class BillingDeskCreateView(generics.ListCreateAPIView):
    queryset = BillingDesk.objects.all()
    serializer_class = BillingDeskSerializer
    permission_classes = [permissions.IsAuthenticated, IsShopOwner]

    def post(self, request, *args, **kwargs):
        data = request.data
        data["assigned_shop"] = request.user
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        print(self.request.user.pk)
        return BillingDesk.objects.filter(assigned_shop = ShopOwner.objects.get(user=self.request.user))

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class ScannerCreateView(generics.ListCreateAPIView):
    queryset = Scanner.objects.all()
    serializer_class = ScannerSerializer
    permission_classes = [permissions.IsAuthenticated, IsBillingDesk, IsShopOwner]


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Handle token-based logout
        if 'rest_framework.authtoken' in settings.INSTALLED_APPS:
            try:
                token = Token.objects.get(user=request.user)
                token.delete()
            except Token.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        # Handle session-based logout
        logout(request)
        return Response(status=status.HTTP_200_OK)
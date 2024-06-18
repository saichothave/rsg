from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
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


class RSGUserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
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
                    return Response({"token": token.key, "user": user.username}, status=200)
                except RSGUser.DoesNotExist:
                    raise UnauthorizedException("Invalid credentials")
            else:
                raise UnauthorizedException("Invalid credentials")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
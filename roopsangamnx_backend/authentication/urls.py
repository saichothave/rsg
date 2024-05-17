# myapp/urls.py
from django.urls import path
from .views import RSGUserCreate, LoginView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('api/register/', RSGUserCreate.as_view(), name='user-create'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/login/', LoginView.as_view(), name='login')
]

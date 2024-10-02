from datetime import datetime
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from django.utils.timezone import now
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


# Not Implemented - syetem should expire tokens daily [Need to revisit]
# current issue - request.user.is_authenticated in returning False for AppUsers
# to implement add import middleware in settings.py - 'authentication.middleware.TokenExpirationMiddleware'
class TokenExpirationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(request.user.is_authenticated)
        if request.user.is_authenticated:
            try:
                token = Token.objects.get(user=request.user)
                # Get current time
                current_time = now()  
                expiration_time = current_time.replace(hour=00, minute=46, second=0, microsecond=0)

                print(token.created.now() < expiration_time.now().date())

                if token.created.now() < expiration_time.now().date():
                    token.delete()  # Optionally, delete the token
                    raise AuthenticationFailed('Token has expired. Please log in again.')
            except Token.DoesNotExist:
                pass  # No token found for this user

        response = self.get_response(request)
        return response
    

class HandleAuthErrorMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Check if the response has a 403 or 401 status code
        if response.status_code == 403:
            return JsonResponse({
                'error': 'Forbidden - You do not have permission to access this resource.',
                'redirect': True,  # Add flag to inform the frontend
                'redirect_url': '/forbidden'  # Set the redirection URL
            }, status=403)
        
        elif response.status_code == 401:
            return JsonResponse({
                'error': 'Unauthorized - Please log in to access this resource.',
                'redirect': True,
                'redirect_url': '/login'  # Set the login URL
            }, status=401)

        return response  # For other responses, just return as-is
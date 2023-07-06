from django.contrib.auth.middleware import AuthenticationMiddleware
from django.http import HttpResponseForbidden

class CustomAuthenticationMiddleware(AuthenticationMiddleware):
    def process_request(self, request):
        # Define the URL that should be excluded from authentication
        excluded_url = ['/signup/', '/login/']
        print(f"Requested path {request.path}")
        # Check if the requested URL matches the excluded URL
        if request.path in excluded_url:
            print("Skipping auth")
            return None  # Skip authentication for this URL

        # For other URLs, continue with the regular authentication process
        return super().process_request(request)
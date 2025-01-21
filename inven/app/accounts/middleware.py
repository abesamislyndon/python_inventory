from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse

class RoleRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        excluded_paths = [
            reverse('login'),  # Login page
            reverse('logout'),  # Logout page
            # reverse('socialaccount_login', kwargs={'provider': 'google'}),  
            # reverse('password_reset'),  # Password reset page (if applicable)
        ]
        # Allow static files (useful during development)
        if request.path.startswith('/static/'):
            return self.get_response(request)

        # Skip role checks for excluded paths
        if request.path in excluded_paths:
            return self.get_response(request)

        # If the user is not authenticated and not on the login page
        if not request.user.is_authenticated:
            if request.path != reverse('login'):
                messages.error(request, "Please log in to access this page.")
                return redirect('login')  # Redirect to login page

        # Check if user is authenticated and authorized (superuser example)
        if request.user.is_authenticated:
            if not request.user.is_superuser:  # Example: allow only superusers
                messages.error(request, "You are not authorized to access this page.")
                return redirect('login')  # Redirect to login page if unauthorized
        # Prevent caching of the page if the user is logged out or unauthorized
        response = self.get_response(request)
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'

        return response

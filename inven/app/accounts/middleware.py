from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse, resolve
from django.http import HttpResponse

class RoleRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define excluded paths
        excluded_paths = [
            reverse('login'),  # Login page
            reverse('logout'),  # Logout page
            reverse('google_login'),  # Google login page
            reverse('account_logout'),  # Allauth logout
        ]

        # Include all allauth-related paths dynamically
        allauth_paths = [
            '/accounts/google/',  # General Google OAuth flow
            '/accounts/social/login/cancelled/',  # Cancelled login
            '/accounts/social/signup/',  # Social signup
            '/events/message_board/',
            '/events/media/guest_messages/',
            '/ws/message_board/',
        ]

        if any(request.path.startswith(path) for path in allauth_paths):
            return self.get_response(request)

        # Allow static files
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            return self.get_response(request)

        # Skip role checks for excluded paths
        if request.path in excluded_paths:
            return self.get_response(request)

        # If user is not authenticated
        if not request.user.is_authenticated:
            if request.path != reverse('login'):
                messages.error(request, "Please log in to access this page.")
                return redirect('login')

        # Role-based check (example: superuser access only)
        if request.user.is_authenticated:
            if not request.user.is_superuser:
                messages.error(request, "You are not authorized to access this page.")
                return redirect('login')

        # No caching for unauthorized users
        response = self.get_response(request)
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'

        return response

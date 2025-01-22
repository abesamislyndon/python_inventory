from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth import logout  
from django.shortcuts import render, redirect

class CustomLoginView(LoginView):
    
    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password. Please try again.")
        return super().form_invalid(form)
    
    
from django.http import HttpResponse

def custom_logout(request):
    # Log the user out
    logout(request)
    # Add a success message after logout
    messages.success(request, "You have successfully logged out.")
    # Create a response that disables caching
    response = redirect('login')  # Make sure 'login' is the correct name
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response

def direct_google_login(request):
    # Redirect to the Google login URL provided by Django Allauth
    return redirect('/accounts/google/login/')

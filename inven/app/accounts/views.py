from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_backends
from django.contrib import messages
from django.contrib.auth import logout  
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .forms import CustomUserCreationForm 

class CustomLoginView(LoginView):
    
    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password. Please try again.")
        return super().form_invalid(form)
    
class RegisterView(FormView):
    template_name = "registration/register.html"  # Path to your registration template
    form_class = CustomUserCreationForm  # Use your custom form
    success_url = "/"  # Redirect to login page after successful registration

    def form_valid(self, form):
        # Save the new user
        user = form.save()

        # Explicitly set the backend (use the first available backend for simplicity)
        backend = get_backends()[0]  # Get the first backend (you can customize this)
        user.backend = f"{backend.__module__}.{backend.__class__.__name__}"

        # Log the user in automatically
        login(self.request, user, backend=user.backend)

        # Add a success message
        messages.success(self.request, "You have successfully registered.")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Add specific error messages
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field.capitalize()}: {error}")
        
        # Render the form with existing data
        return self.render_to_response(self.get_context_data(form=form))
    
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

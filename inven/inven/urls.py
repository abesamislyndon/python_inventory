from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
     path('', LoginView.as_view(template_name='accounts/login.html'), name='login'),
     path('dashboards/', include('app.dashboards.urls')), 
     path("__reload__/", include("django_browser_reload.urls")), # Correct
]

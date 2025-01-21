from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
     # path('', LoginView.as_view(template_name='accounts/login.html'), name='login'),
     path('', include('app.accounts.urls')),  
     path('dashboards/', include('app.dashboards.urls')), 
     path('events/', include('app.clients.urls')),
   
     #   path('dashboard/', views.admin_dashboard, {'required_role': 'Admin'}, name='admin_dashboard'),
]


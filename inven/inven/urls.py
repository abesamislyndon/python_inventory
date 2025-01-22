from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     # path('', LoginView.as_view(template_name='accounts/login.html'), name='login'),
     path('', include('app.accounts.urls')),  
     path('dashboards/', include('app.dashboards.urls')), 
     path('events/', include('app.clients.urls')),
   
     #   path('dashboard/', views.admin_dashboard, {'required_role': 'Admin'}, name='admin_dashboard'),
]


if settings.DEBUG:  # Serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
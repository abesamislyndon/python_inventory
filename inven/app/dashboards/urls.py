from django.urls import path
from . import views  # Import views from the same app

urlpatterns = [
     path('', views.dashboard_home, name='dashboard_home'),  # Example route
    # path('', views.dashboard_home, {'required_role': 'Admin'}, name='dashboard_home'),
]



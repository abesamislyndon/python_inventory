from django.urls import path
from django.contrib.auth import views as auth_views
from app.accounts.views import CustomLoginView, custom_logout
from django.urls import path, include
from django.shortcuts import redirect


urlpatterns = [
    path('', CustomLoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', custom_logout, name='logout'),
    path('accounts/', include('allauth.urls')),
    # path('login/google/', direct_google_login, name='direct_google_login'),
    path('accounts/google/login/', lambda request: redirect('socialaccount_login', provider='google')),
]









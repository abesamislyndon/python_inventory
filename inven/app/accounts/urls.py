from django.urls import path
from . import views


urlpatterns = [
    path('register-account', views.register_account, name="register_account"),
    path('reset-password', views.reset_password, name="reset_password")

]
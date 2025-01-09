from django.urls import path
from  . import views

urlpatterns = [
    path('', views.clients_index, name = "clients"),
    path('new', views.client_form, name = "new"),
    path('create', views.create, name='create'),
]
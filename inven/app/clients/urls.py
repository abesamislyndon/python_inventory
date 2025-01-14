from django.urls import path
from  . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.clients_index, name = "clients"),
    path('new', views.client_form, name = "new"),
    path('create', views.create, name='create'),
    path('success_msg/', views.success_msg, name='success_msg'),
    path('message_board/', views.message_board, name='message_board'),
    path("submit_message/", views.message_form, name="submit_message"),
    path('<str:client_url>/', views.msg_board, name="client_detail"),
    path('<str:client_url>/guest-message/', views.guest_message_view, name='guest_message'),
    path('api/messages/<str:client_url>/', views.get_client_msgs_json, name='get_client_msgs_json'),
     
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
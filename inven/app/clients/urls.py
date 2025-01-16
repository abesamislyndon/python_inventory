from django.urls import path
from  . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.events_index, name = "events"),
    path('new', views.client_form, name = "new"),
    path('create', views.create, name='create'),
    path('message_board/<str:client_url>/', views.message_board, name='message_board'),
    path("submit_message/<str:client_url>/", views.message_form, name="submit_message"),
    path("success_msg/<str:client_url>/", views.success_msg, name="success_msg"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
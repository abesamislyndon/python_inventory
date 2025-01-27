from django.shortcuts import render
from django.utils import timezone
from ..clients.models import Client, ClientMsg

def dashboard_home(request):
    user = request.user
    event_count = Client.objects.filter(user=user).count()
    msg_count =  ClientMsg.objects.filter(client__user=user).count()
    today = timezone.now().date()   
    event_count_today = Client.objects.filter(created_at__date=today, user=user).count()

    return render(request, 'dashboards/dashboard.html', {'event_count': event_count, "msg_count": msg_count, "event_count_today": event_count_today}) 

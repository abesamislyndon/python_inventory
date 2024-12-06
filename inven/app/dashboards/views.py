from django.shortcuts import render

def dashboard_home(request):
    return render(request, 'dashboards/dashboard.html')  # Render a template for the dashboard

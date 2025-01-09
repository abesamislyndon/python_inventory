from django.shortcuts import render, get_object_or_404, redirect
from .forms import ClientForm
from .models import Client


def clients_index(request):
    client_list = { 'client_list': Client.objects.all() }
    return render(request, 'clients/index.html', client_list)


def client_form(request):
    form  = ClientForm 
    return render(request, 'clients/client_form.html', {"form":form})

def create(request):
    
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clients')
        else:
            form = ClientForm
            return render(request, 'clients/client_form.html', { 'form': form}) 
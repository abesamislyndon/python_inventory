from django.shortcuts import render, get_object_or_404, redirect
from .models import Client, ClientMsg
from .forms import ClientForm, GuestForm
from django.http import JsonResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from asgiref.sync import sync_to_async
import logging


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
        
def msg_board(request, client_url):
    # Fetch the client with the given client_url
    client = get_object_or_404(Client, client_url=client_url)
    
    # Fetch messages associated with this client
    client_msgs = ClientMsg.objects.filter(client=client).order_by('-created_at')  # Order by most recent messages first
    
    # Pass the client and messages to the template
    return render(request, 'clients/msg_board.html', {'client': client, 'client_msgs': client_msgs})

def guest_message_view(request, client_url):
    # Get the client object or return a 404 if not found
    client = get_object_or_404(Client, client_url=client_url)
    
    # Handle form submission
    if request.method == 'POST':
        form = GuestForm(request.POST, request.FILES)
        if form.is_valid():
            guest_msg = form.save(commit=False)  # Save the form but don't commit yet
            guest_msg.client = client  # Associate the message with the client
            guest_msg.save()  # Save the message to the database
            
            # Check if the request is an AJAX request by looking at the header
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'message': 'Success', 'guest_msg': guest_msg.to_dict()})
            
            # Redirect to a success page after submission if not using AJAX
            return redirect('success_msg/')
    else:
        form = GuestForm()

    # Retrieve previous messages for the client
    client_msgs = ClientMsg.objects.filter(client=client).order_by('-created_at')

    # Render the form along with the client information and previous messages
    return render(request, 'clients/guest_message.html', {
        'form': form,
        'client': client,
        'client_msgs': client_msgs,
    })

def success_msg(request):
    return render(request, 'clients/success_msg.html')

def get_client_msgs_json(request , client_url):
    client = get_object_or_404(Client, client_url=client_url)
    client_msgs = ClientMsg.objects.filter(client=client).order_by('-created_at')  # Fetch messages
    
 # Serialize messages into a list of dictionaries including unique id
    messages = [
        {
            'id': msg.id,  # Include unique ID for each message
            'guest_name': msg.guest_name,
            'content': msg.content,
            'created_at': msg.created_at,
            'image_url': msg.image.url if msg.image else None
        }
        for msg in client_msgs
    ]

    # Return messages as JSON
    return JsonResponse({'messages': messages})
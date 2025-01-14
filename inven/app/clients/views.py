from django.shortcuts import render, get_object_or_404, redirect
from .models import Client, ClientMsg
from .forms import ClientForm, GuestForm
from django.http import JsonResponse

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer



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


def success_msg(request):
    return render(request, 'clients/success_msg.html')

def post_list(request):
    return render(request, 'clients/template.html')



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

            # Push the new message to the WebSocket
            send_new_client_msg_to_websocket(guest_msg)

            # Check if the request is an AJAX request by looking at the header
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'message': 'Success',
                    'guest_msg': guest_msg.to_dict()  # Convert the message to dict (add to_dict method in model)
                })
            
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

# Function to send new client messages to the WebSocket
def send_new_client_msg_to_websocket(guest_msg):
    from channels.layers import get_channel_layer
    channel_layer = get_channel_layer()
    
    # Format message data
    message_data = {
        'id': guest_msg.id,
        'guest_name': guest_msg.guest_name,
        'content': guest_msg.content,
        'image_url': guest_msg.image.url if guest_msg.image else '',
        'created_at': guest_msg.created_at.isoformat(),  # You can format this as needed
    }
    
    # Send the message to the WebSocket
    channel_layer.group_send(
        f'client_messages_group_{guest_msg.client.id}',  # Group name based on the client ID
        {
            'type': 'send_message',  # Handler in WebSocket consumer
            'message': message_data,
        }
    )

def message_board(request, client_url):
    # Fetch the client based on the client_url
    client = get_object_or_404(Client, client_url=client_url)
    # messages = ClientMsg.objects.filter(client=client).select_related('client').order_by('-created_at')
    messages = ClientMsg.objects.filter(client=client).order_by('-created_at')
    return render(request, "clients/message_board.html", {"client": client, "messages": messages})

def message_form(request, client_url):
    # Fetch the client based on client_url
    client = get_object_or_404(Client, client_url=client_url)

    if request.method == "POST":
        guest_name = request.POST.get("guest_name")
        content = request.POST.get("content")
        image = request.FILES.get("image")

        if guest_name and content:
            # Create a new message for the specific client
            message = ClientMsg.objects.create(
                guest_name=guest_name,
                client=client,
                content=content,
                image=image,
            )

            # Broadcasting the new message via WebSocket
            from asgiref.sync import async_to_sync
            from channels.layers import get_channel_layer
            channel_layer = get_channel_layer()

            async_to_sync(channel_layer.group_send)(
                f"message_board_{client.client_url}",
                {
                    "type": "new_message",
                    "message": {
                        "guest_name": message.guest_name,
                        "client_name": message.client.client_name,
                        "content": message.content,
                        "image_url": message.image.url if message.image else "",
                        "created_at": message.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    },
                },
            )

            return JsonResponse({"status": "success"}, status=200)

    return render(request, "clients/message_form.html", {"client": client})
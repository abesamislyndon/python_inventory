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

def create(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            # Save the new message
            new_client_msg = form.save()

            # Trigger sending the message to WebSocket after saving
            new_client_msg.send_new_client_msg_to_websocket()

            return redirect('clients')
        else:
            return render(request, 'clients/client_form.html', {'form': form})
    else:
        form = ClientForm()
        return render(request, 'clients/client_form.html', {'form': form})
        
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

def submit_client_msg(request):
    if request.method == "POST":
        guest_name = request.POST.get('guest_name')
        client_id = request.POST.get('client_id')
        content = request.POST.get('content')
        
        # Create a new ClientMsg instance
        client_msg = ClientMsg.objects.create(
            guest_name=guest_name,
            client_id=client_id,
            content=content
        )

        # Trigger the WebSocket message broadcasting after saving to the DB
        send_new_client_msg_to_websocket(client_msg.id)

        return JsonResponse({"success": True, "message": client_msg.content})
    
    return JsonResponse({"success": False}, status=400)




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



def message_board(request):
    messages = ClientMsg.objects.select_related('client').all().order_by('-created_at')

    return render(request, "clients/message_board.html", {"messages": messages})


def message_form(request):
    if request.method == "POST":
        guest_name = request.POST.get("guest_name")
        client_id = request.POST.get("client")
        content = request.POST.get("content")
        image = request.FILES.get("image")

        if guest_name and client_id and content:
            client = Client.objects.get(pk=client_id)
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
                "message_board",
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

    clients = Client.objects.all()
    return render(request, "clients/message_form.html", {"clients": clients})
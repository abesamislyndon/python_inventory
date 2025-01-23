from django.shortcuts import render, get_object_or_404, redirect
from .models import Client, ClientMsg
from .forms import ClientForm
from .forms import MessageBoardForm
from inven.utils import dynamic_url, generate_qrcode
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# CLIENT LIST
def events_index(request):

    Events =  Client.objects.filter(user=request.user)
    client_list = { 'client_list': Events.all() }
    return render(request, 'clients/index.html', client_list)

# CLIENT CRUD - READ
def client_form(request):
    form  = ClientForm 
    return render(request, 'clients/client_form.html', {"form":form})

#CLIENT CRUD - CREATE
@login_required
def create_or_edit_client(request, client_id=None):
    if client_id:
        # If `client_id` is provided, fetch the existing Client for editing
        client = get_object_or_404(Client, id=client_id, user=request.user)
    else:
        # Otherwise, create a new Client instance for creation
        client = None

    if request.method == 'POST':
        # If it's a POST request, handle form submission
        form = ClientForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            client = form.save(commit=False)
            client.user = request.user  # Assign the current user to the client
            client.save()
            
            # Add a success message for SweetAlert
            if client_id:
                messages.success(request, 'Event updated successfully!')
            else:
                messages.success(request, 'Event created successfully!')

            return redirect(request.path)   # Redirect to the events page or another appropriate view
    else:
        # If it's a GET request, prefill the form with instance data (if editing)
        form = ClientForm(instance=client)

    # Render the form template
    return render(request, 'clients/client_form.html', {'form': form, 'client': client})

def delete_event(request, client_id):
    try:
        event = Client.objects.get(id=client_id)
        event.delete()
        messages.success(request, 'Event deleted successfully.')
    except Client.DoesNotExist:
        messages.error(request, 'Event not found.')

    return redirect('events')  # Replace with your event list page URL

# client success
def success_msg(request, client_url):
    client = get_object_or_404(Client, client_url=client_url)
    return render(request, 'events/success_msg.html',{"client" : client})

# SPECIFIC CLIENT MESSAGE BOARD
def message_board(request, client_url):
    # Fetch the client based on the client_url
    client = get_object_or_404(Client, client_url=client_url)
    theme_settings = client.theme_settings
    messages = ClientMsg.objects.filter(client=client).order_by('-created_at')
    return render(request, "clients/message_board.html", {"client": client, "messages": messages, "theme_settings": theme_settings})

# GUEST FORMS FOR A SPECIC CLIENT
def message_form(request, client_url):
    # Fetch the client based on client_url
    client = get_object_or_404(Client, client_url=client_url)
    theme_settings = client.theme_settings

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
                        "event_name": message.client.event_name,
                        "content": message.content,
                        "image_url": message.image.url if message.image else "",
                        "created_at": message.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    },
                },
            )
            # return JsonResponse({"status": "success"}, status=200)
            return render(request, "clients/success_msg.html", {"client": client})
    return render(request, "clients/message_form.html", {"client": client,  "theme_settings": theme_settings})


def event_settings(request, client_url):
    client = get_object_or_404(Client, client_url=client_url)
    full_url_form = dynamic_url(request, 'submit_message', client_url)
    full_url_photo_wall = dynamic_url(request, 'message_board', client_url)
    qr_code_forms = generate_qrcode(full_url_form)
    qr_code_wall = generate_qrcode(full_url_photo_wall)

    if request.method == "POST":
        form = MessageBoardForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()
            return redirect("event_settings", client_url=client.client_url)
        else:
            print("Form is invalid. Errors:", form.errors)
    else:
        form = MessageBoardForm(instance=client)

    return render(request, "clients/event_settings.html", {"form": form, "client": client, "full_url": full_url_form, "full_url_wall":full_url_photo_wall, "qr_image": qr_code_forms, "qr_image_wall": qr_code_wall})

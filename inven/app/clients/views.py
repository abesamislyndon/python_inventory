from django.shortcuts import render, get_object_or_404, redirect
from .models import Client, ClientMsg
from .forms import ClientForm, GuestForm
from django.http import JsonResponse
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


# CLIENT LIST
def events_index(request):
    client_list = { 'client_list': Client.objects.all() }
    return render(request, 'clients/index.html', client_list)

# CLIENT CRUD - READ
def client_form(request):
    form  = ClientForm 
    return render(request, 'clients/client_form.html', {"form":form})

#CLIENT CRUD - CREATE
def create(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clients')
        else:
            form = ClientForm
            return render(request, 'clients/client_form.html', { 'form': form}) 

def success_msg(request, client_url):
    client = get_object_or_404(Client, client_url=client_url)
    return render(request, 'clients/success_msg.html',{"client" : client})

# SPECIFIC CLIENT MESSAGE BOARD
def message_board(request, client_url):
    # Fetch the client based on the client_url
    client = get_object_or_404(Client, client_url=client_url)
    # messages = ClientMsg.objects.filter(client=client).select_related('client').order_by('-created_at')
    messages = ClientMsg.objects.filter(client=client).order_by('-created_at')
    return render(request, "clients/message_board.html", {"client": client, "messages": messages})

# GUEST FORMS FOR A SPECIC CLIENT
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

            # return JsonResponse({"status": "success"}, status=200)
            return render(request, "clients/success_msg.html", {"client": client})

    return render(request, "clients/message_form.html", {"client": client})
# models.py
from django.db import models

# Event model
class Client(models.Model):
    event_name = models.CharField(max_length=100)  # Renamed from client_name
    guest_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    client_url = models.CharField(max_length=255, null=True, blank=True)
    event_date = models.DateTimeField(null=True, blank=True)
    event_type = models.CharField(max_length=100, null=True, blank=True)
    event_logo = models.ImageField(upload_to='event_logos/', blank=True, null=True)
    # theme_settings = models.JSONField(default=dict) 
    theme_settings = models.JSONField(default=dict, blank=True)
    
#Event Message
class ClientMsg(models.Model):
    guest_name = models.CharField(max_length=100)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)  # Corrected field name
    content = models.TextField()
    image = models.ImageField(upload_to='guest_messages/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.guest_name}: {self.content[:50]}"


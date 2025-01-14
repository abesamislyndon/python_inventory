# models.py

from django.db import models

class Client(models.Model):
    client_name = models.CharField(max_length=100)
    guest_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    client_url = models.CharField(null=True, blank=True)
    

    
class ClientMsg(models.Model):
    guest_name = models.CharField(max_length=100)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)  # Corrected field name
    content = models.TextField()
    image = models.ImageField(upload_to='guest_messages/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.guest_name}: {self.content[:50]}"


# models.py
from django.contrib.auth.models import User
from django.db import models
from PIL import Image
import os
import pillow_heif  # Import this to enable HEIC support in Pillow


# Event model
class Client(models.Model):
    event_name = models.CharField(max_length=100)  # Renamed from client_name
    guest_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    client_url = models.CharField(max_length=255, unique=True, null=True, blank=True)
    event_date = models.DateTimeField(null=True, blank=True)
    event_type = models.CharField(max_length=100, null=True, blank=True)
    event_logo = models.ImageField(upload_to='event_logos/', blank=True, null=True)
    # theme_settings = models.JSONField(default=dict) 
    theme_settings = models.JSONField(default=dict, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients',  blank=True, null=True)
    
#Event Message
class ClientMsg(models.Model):
    guest_name = models.CharField(max_length=100)
    client = models.ForeignKey('Client', on_delete=models.CASCADE)  # Ensure Client is defined in your app
    content = models.TextField()
    image = models.ImageField(upload_to='guest_messages/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.guest_name}: {self.content[:50]}"
    
    def save(self, *args, **kwargs):
        # Save the instance first to generate the image path
        super().save(*args, **kwargs)
        
        # Convert HEIC to JPEG if necessary
        if self.image and self.image.path.lower().endswith('.heic'):
            self.convert_heic_to_jpeg()

    def convert_heic_to_jpeg(self):
        image_path = self.image.path
        
        # Open the HEIC image using Pillow (with pillow-heif plugin)
        pillow_heif.register_heif_opener()  # Ensure HEIC support is registered
        with Image.open(image_path) as img:
            # Define the new file path with .jpeg extension
            jpeg_path = os.path.splitext(image_path)[0] + '.jpeg'
            img.save(jpeg_path, format='JPEG')  # Save as JPEG
            
            # Update the model's image field to point to the new file
            self.image.name = os.path.splitext(self.image.name)[0] + '.jpeg'
            self.save()  # Save the updated instance
            
            # Remove the original HEIC file
            os.remove(image_path)


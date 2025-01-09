from django.contrib.auth.models import AbstractUser
from django.db import models


class Post(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='uploads/')
    message = models.TextField()
    is_approved = models.BooleanField(default=False)  # Admin approval
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
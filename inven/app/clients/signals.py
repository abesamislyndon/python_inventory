# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Post
# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer

# @receiver(post_save, sender=Post)
# def notify_post_created(sender, instance, created, **kwargs):
#     if created:
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             'posts',
#             {
#                 'type': 'post_message',
#                 'message': f"New post: {instance.title}"
#             }
#         )

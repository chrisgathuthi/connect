from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Room


@receiver(post_save, sender=Room)
def send_notification(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        group_name = "user-notification"
        event = {
            "type": "user_joined",
            "text": instance.name
        }
        async_to_sync(channel_layer.group_send)(group_name, event)

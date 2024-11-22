from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Component, Room

channel_layer = get_channel_layer()


@receiver(post_save, sender=Room)
def room_saved(sender, instance, **kwargs):
    # Envia a mensagem para o grupo rooms_group
    async_to_sync(channel_layer.group_send)(
        "rooms_group",
        {
            "type": "send_rooms_updated",
        },
    )


@receiver(post_delete, sender=Room)
def room_deleted(sender, instance, **kwargs):
    # Envia a mensagem para o grupo rooms_group
    async_to_sync(channel_layer.group_send)(
        "rooms_group",
        {
            "type": "send_rooms_updated",
        },
    )


@receiver(post_save, sender=Component)
def component_saved(sender, instance, **kwargs):
    # Envia a mensagem para o grupo components_group
    async_to_sync(channel_layer.group_send)(
        "components_group",
        {
            "type": "send_components_updated",
        },
    )


@receiver(post_delete, sender=Component)
def component_deleted(sender, instance, **kwargs):
    # Envia a mensagem para o grupo components_group
    async_to_sync(channel_layer.group_send)(
        "components_group",
        {
            "type": "send_components_updated",
        },
    )

import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from celery import shared_task

@shared_task
def handle_book_added_event(event_data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "catalogue_updates",
        {"type": "book.added", "data": event_data}
    )
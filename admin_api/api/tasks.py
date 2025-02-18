from celery import shared_task
import json
from django.core.serializers.json import DjangoJSONEncoder
from .models import Book

@shared_task
def notify_frontend_of_book_change(book_id):
    from .models import Book
    try:
        book = Book.objects.get(id=book_id)
        book_data = {
            'id': book.id,
            'title': book.title,
            'publisher': book.publisher,
            'category': book.category,
            'is_available': book.is_available,
            'expected_return_date': book.expected_return_date
        }
        
        # Send message to Redis channel
        from channels.layers import get_channel_layer
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "catalogue_updates",
            {"type": "book.update", "data": book_data}
        )
        
        return True
    except Book.DoesNotExist:
        return False
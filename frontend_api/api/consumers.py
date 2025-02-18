# frontend_api/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Book

class CatalogueUpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join room group
        self.room_group_name = 'catalogue_updates'
        
        # Join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
    
    # Receive message from room group
    async def book_update(self, event):
        book_data = event['data']
        
        # Update local database
        try:
            book, created = Book.objects.get_or_create(id=book_data['id'])
            book.title = book_data['title']
            book.publisher = book_data['publisher']
            book.category = book_data['category']
            book.is_available = book_data['is_available']
            book.expected_return_date = book_data['expected_return_date']
            book.save()
            
            # Send confirmation to WebSocket
            await self.send(text_data=json.dumps({
                'message': 'Book updated successfully',
                'book_id': book.id
            }))
        except Exception as e:
            await self.send(text_data=json.dumps({
                'error': str(e)
            }))
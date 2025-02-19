# frontend_api/views.py
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import User, Book, BorrowRecord
from .serializers import UserSerializer, BookSerializer, BorrowRecordSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets
import pika
from datetime import datetime, timedelta

# Connect to RabbitMQ
def publish_message(event, data):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue="borrow_updates", durable=True)
    message = json.dumps({"event": event, "data": data})
    channel.basic_publish(exchange="", routing_key="borrow_updates", body=message)
    connection.close()

class UserRegistrationView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Book.objects.filter(is_available=True)
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['publisher', 'category']
    search_fields = ['title', 'publisher', 'category']
    ordering_fields = ['title', 'publisher']

class SingleBookView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BorrowBookView(APIView):
    def post(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
            
            if not book.is_available:
                return Response({
                    'error': 'Book is currently unavailable',
                    'expected_return_date': book.expected_return_date
                }, status=status.HTTP_400_BAD_REQUEST)
                
            borrow_days = int(request.data.get('days', 14))
            expected_return_date = self._calculate_return_date(borrow_days)
            
            book.is_available = False
            book.expected_return_date = expected_return_date
            book.save()

            # Create borrowing record
            BorrowRecord.objects.create(
                user=request.user,
                book=book,
                expected_return_date=expected_return_date
            )
            
            return Response({
                'message': 'Book borrowed successfully',
                'return_date': expected_return_date
            })
            
        except Book.DoesNotExist:
            return Response({
                'error': 'Book not found'
            }, status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer):
        book = serializer.save()
        publish_message("book_borrowed", {"book_id": book.id})

    def _calculate_return_date(self, days):
        return datetime.now() + timedelta(days=days)
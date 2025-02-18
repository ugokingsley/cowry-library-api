from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from .models import Book, User, BorrowRecord
from .serializers import AdminBookSerializer, UserManagementSerializer, BorrowStatusSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets
from .tasks import notify_frontend_of_book_change



class AdminBookViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = AdminBookSerializer
    queryset = Book.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['title', 'publisher', 'category']
    ordering_fields = ['title', 'publisher']

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            book = serializer.save()
            
            task_id = notify_frontend_of_book_change.delay(book.id).id
            
            return Response({
                'message': 'Book added successfully',
                'task_id': task_id,
                'book_id': book.id
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserManagementView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserManagementSerializer
    queryset = User.objects.all()
    filter_backends = [OrderingFilter]
    ordering_fields = ['email', 'first_name', 'last_name']


class UnavailableBooksView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BorrowStatusSerializer
    
    def get_queryset(self):
        return Book.objects.filter(is_available=False)

class BorrowingStatusView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BorrowStatusSerializer
    
    def get_queryset(self):
        return BorrowRecord.objects.select_related('book', 'user')
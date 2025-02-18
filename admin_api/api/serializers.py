from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book, BorrowRecord

class AdminBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'publisher',
            'category',
            'is_available',
            'expected_return_date'
        ]

class UserManagementSerializer(serializers.ModelSerializer):
    borrowed_books_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'borrowed_books_count'
        ]
        
    def get_borrowed_books_count(self, obj):
        return BorrowRecord.objects.filter(
            user=obj,
            actual_return_date__isnull=True
        ).count()

class BorrowStatusSerializer(serializers.ModelSerializer):
    book_title = serializers.ReadOnlyField(source='book.title')
    borrower_name = serializers.SerializerMethodField()
    
    class Meta:
        model = BorrowRecord
        fields = [
            'id',
            'book',
            'book_title',
            'borrower_name',
            'borrow_date',
            'expected_return_date',
            'actual_return_date'
        ]
        
    def get_borrower_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
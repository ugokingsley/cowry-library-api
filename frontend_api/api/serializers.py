from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        if 'username' not in validated_data:
            validated_data['username'] = validated_data['email'].split('@')[0]  
        user = User.objects.create_user(**validated_data)
        return user

class BookSerializer(serializers.ModelSerializer):
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
        read_only_fields = ['is_available', 'expected_return_date']

class BorrowRecordSerializer(serializers.ModelSerializer):
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
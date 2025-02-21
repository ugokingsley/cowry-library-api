import pytest
from django.contrib.auth import get_user_model
from api.models import Book, BorrowedBook
from datetime import date, timedelta

User = get_user_model()

@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(email="test@example.com", first_name="John", last_name="Doe", password="password123")
    assert user.email == "test@example.com"
    assert user.first_name == "John"
    assert user.check_password("password123")

@pytest.mark.django_db
def test_create_book():
    book = Book.objects.create(title="Python for Beginners", author="John Doe", publisher="Apress", category="Technology")
    assert book.title == "Python for Beginners"
    assert book.available is True

@pytest.mark.django_db
def test_borrow_book():
    user = User.objects.create_user(email="user@example.com", first_name="Jane", last_name="Doe", password="password")
    book = Book.objects.create(title="Django Unleashed", author="Andrew Pinkham", publisher="Manning", category="Technology")
    
    borrowed_book = BorrowedBook.objects.create(user=user, book=book, borrowed_until=date.today() + timedelta(days=7))
    assert borrowed_book.user == user
    assert borrowed_book.book == book
    assert borrowed_book.borrowed_until > date.today()

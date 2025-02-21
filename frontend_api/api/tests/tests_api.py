import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from api.models import Book

User = get_user_model()

@pytest.mark.django_db
def test_register_user():
    client = APIClient()
    response = client.post("/users/", {"email": "test@user.com", "first_name": "John", "last_name": "Doe", "password": "securepassword"})
    assert response.status_code == 201
    assert response.data["email"] == "test@user.com"

@pytest.mark.django_db
def test_list_books():
    Book.objects.create(title="Python Basics", author="Guido van Rossum", publisher="O'Reilly", category="Technology")
    client = APIClient()
    response = client.get("/books/")
    assert response.status_code == 200
    assert len(response.data) == 1

@pytest.mark.django_db
def test_filter_books():
    Book.objects.create(title="Deep Learning", author="Ian Goodfellow", publisher="MIT Press", category="Science")
    client = APIClient()
    response = client.get("/books/?category=Science")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["title"] == "Deep Learning"

@pytest.mark.django_db
def test_borrow_book():
    client = APIClient()
    user = User.objects.create_user(email="user@example.com", first_name="Jane", last_name="Doe", password="password")
    book = Book.objects.create(title="Machine Learning", author="Andrew Ng", publisher="Stanford", category="Technology")
    
    client.force_authenticate(user=user)
    response = client.post("/borrow/", {"book": book.id, "borrowed_until": "2025-02-25"})
    assert response.status_code == 201

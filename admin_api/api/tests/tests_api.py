import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from api.models import Book

@pytest.mark.django_db
def test_admin_add_book():
    client = APIClient()
    admin = User.objects.create_superuser(username="admin", password="adminpassword")
    client.force_authenticate(user=admin)
    
    response = client.post("/books/", {"title": "Django Mastery", "author": "William Vincent", "publisher": "Apress", "category": "Technology", "available": True})
    assert response.status_code == 201
    assert Book.objects.count() == 1

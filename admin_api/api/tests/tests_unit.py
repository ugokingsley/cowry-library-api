import pytest
from .models import Book

@pytest.mark.django_db
def test_create_book():
    book = Book.objects.create(title="Advanced Python", author="David Beazley", publisher="O'Reilly", category="Technology")
    assert book.title == "Advanced Python"
    assert book.publisher == "O'Reilly"
    assert book.available is True

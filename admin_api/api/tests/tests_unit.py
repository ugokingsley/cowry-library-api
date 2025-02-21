import pytest
from api.models import *

@pytest.mark.django_db
def test_create_book():
    book = Book.objects.create(title="Advanced Python", publisher="O'Reilly", category="Technology")
    assert book.title == "Advanced Python"
    assert book.publisher == "O'Reilly"
    assert book.is_available is True

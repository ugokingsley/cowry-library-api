from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

class Book(models.Model):
    title = models.CharField(max_length=200)
    publisher = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    expected_return_date = models.DateField(null=True, blank=True)

class BorrowRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
from django.urls import path
from rest_framework.routers import DefaultRouter
from api import views
from django.contrib import admin

router = DefaultRouter()
router.register(r'books', views.BookViewSet, basename='books')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('books/<int:pk>/', views.SingleBookView.as_view(), name='single-book'),
    path('borrow/<int:book_id>/', views.BorrowBookView.as_view(), name='borrow-book'),
] + router.urls
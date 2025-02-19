from django.urls import path
from rest_framework.routers import DefaultRouter
from api import views
from django.contrib import admin

router = DefaultRouter()
router.register(r'books', views.BookViewSet, basename='books')
router.register(r'borrow', views.BorrowBookView, basename='borrow-book')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
] + router.urls
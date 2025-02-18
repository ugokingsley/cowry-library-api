from django.urls import path
from rest_framework.routers import DefaultRouter
from api import views
from django.contrib import admin

router = DefaultRouter()
router.register(r'books', views.AdminBookViewSet, basename='admin-books')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', views.UserManagementView.as_view(), name='users'),
    path('books/unavailable/', views.UnavailableBooksView.as_view(), name='unavailable-books'),
    path('borrowings/', views.BorrowingStatusView.as_view(), name='borrowing-status'),
] + router.urls
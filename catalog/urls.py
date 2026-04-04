from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/<int:pk>/review/', views.add_review, name='add_review'),
    path('reading-lists/', views.reading_list_view, name='reading_lists'),
    path('reading-lists/create/', views.create_reading_list, name='create_reading_list'),
    path('trending/', views.trending_books, name='trending_books'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='reports-dashboard'),
    path('most-borrowed/', views.most_borrowed_books, name='most-borrowed'),
    path('circulation/', views.circulation_statistics, name='circulation-stats'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('loans/', views.my_loans, name='my_loans'),
    path('checkout/', views.checkout_book, name='checkout_book'),
    path('return/<int:loan_id>/', views.return_book, name='return_book'),
    path('renew/<int:loan_id>/', views.renew_loan, name='renew_loan'),
    path('reservations/', views.my_reservations, name='my_reservations'),
    path('reserve/<int:book_id>/', views.create_reservation, name='create_reservation'),
    path('fines/', views.my_fines, name='my_fines'),
]

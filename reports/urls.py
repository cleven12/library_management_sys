from django.urls import path
from . import views

urlpatterns = [
    path('circulation/', views.circulation_report, name='circulation_report'),
    path('overdue/', views.overdue_report, name='overdue_report'),
    path('revenue/', views.revenue_report, name='revenue_report'),
]

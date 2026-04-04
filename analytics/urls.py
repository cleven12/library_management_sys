from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='analytics_dashboard'),
    path('popular-books/', views.popular_books_report, name='popular_books'),
    path('members/', views.member_analytics, name='member_analytics'),
    path('statistics/', views.statistics_report, name='statistics_report'),
    path('my-stats/', views.my_reading_stats, name='my_reading_stats'),
]

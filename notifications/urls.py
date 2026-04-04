from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification_list, name='notification_list'),
    path('read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
    path('preferences/', views.notification_preferences, name='notification_preferences'),
]

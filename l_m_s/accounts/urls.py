from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_member, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('activity/', views.activity_log_view, name='activity_log'),
]

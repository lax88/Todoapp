# users/urls.py
from django.urls import path
from .views import register_view, login_view

urlpatterns = [
    path('register/', register_view, name='register'),  # Use the new register_view
    path('login/', login_view, name='login'),
]

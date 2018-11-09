from django.urls import path
from accounts import views

urlpatterns = [
    path('register/', views.signup, name='register'),
]
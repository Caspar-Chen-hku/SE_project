from django.urls import path
from accounts import views

urlpatterns = [
    path('clinic_manager/register/', views.signup_cm, name='register-cm'),
    path('warehouse_personnel/register/', views.signup_wp, name='register-wp'),
    path('dispatcher/register/', views.signup_d, name='register-d'),
    path('register/', views.authentication, name='auth-token'),
    path('admin', views.adminSendToken, name='send-token'),
]
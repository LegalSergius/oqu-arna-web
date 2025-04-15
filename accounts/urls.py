from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('register/', views.RegisterView.as_view(), name='register'),
    path('register_code/', views.RegisterCodeView.as_view(), name='register-code'),
    path('register_set_password/', views.RegisterSetPasswordView.as_view(), name='register-set-password'),

    path('', views.HomeView.as_view(), name='home'),
]
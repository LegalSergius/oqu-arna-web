from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [

    path('send_code', views.SendCodeToEmailView.as_view(), name='send-code'),

    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('verification_code/', views.VerificationCodeView.as_view(), name='verification-code'),
    path('registration_set_password/', views.RegistrationSetPasswordView.as_view(), name='register-set-password'),

    path('', views.HomeView.as_view(), name='home'),
]
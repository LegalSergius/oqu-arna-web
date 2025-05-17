from .views import ActivateUserPasswordResetConfirmView

from django.urls import path, include

from . import views

app_name = "users"

urlpatterns = [
    path(
        'activate/<uidb64>/<token>/',
        ActivateUserPasswordResetConfirmView.as_view(),
        name='activate'
    ),

    path('send_code', views.SendCodeToEmailView.as_view(), name='send-code'),

    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('entry_email/', views.EntryEmailView.as_view(), name='entry-email'),
    path('verification_code/', views.VerificationCodeView.as_view(), name='verification-code'),
    path('reset_password/', views.ResetPasswordView.as_view(), name='reset-password'),

    path('register_entry_email/', views.RegisterEntryEmailView.as_view(), name='register-entry-email'),
    path('register_verification_code/', views.RegisterVerificationCodeView.as_view(), name='register-verification-code'),
    path('register_set_password/', views.RegisterResetPasswordView.as_view(), name='register-set-password'),
    path('', views.HomeView.as_view(), name='home'),
]

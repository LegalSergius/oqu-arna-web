from .views import ActivateUserPasswordResetConfirmView

from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    # активация учётной записи
    path(
        "activate/<uidb64>/<token>/",
        views.ActivateUserPasswordResetConfirmView.as_view(),
        name="activate",
    ),

    path('send_code', views.SendCodeToEmailView.as_view(), name='send-code'),

    # профиль, аватар и документы
    path("profile/",               views.ProfileView.as_view(),     name="profile"),
    path("profile/avatar/",        views.UpdateAvatarView.as_view(), name="update-avatar"),
    path("profile/avatar/delete/", views.DeleteAvatarView.as_view(), name="delete-avatar"),

    path('entry_email/', views.EntryEmailView.as_view(), name='entry-email'),
    path('verification_code/', views.VerificationCodeView.as_view(), name='verification-code'),
    path('reset_password/', views.ResetPasswordView.as_view(), name='reset-password'),

    path('register_entry_email/', views.RegisterEntryEmailView.as_view(), name='register-entry-email'),
    path('register_verification_code/', views.RegisterVerificationCodeView.as_view(), name='register-verification-code'),
    path('register_set_password/', views.RegisterResetPasswordView.as_view(), name='register-set-password'),
    path('', views.HomeView.as_view(), name='home'),
    # документы пользователя
    path("profile/documents/",               views.DocumentsView.as_view() ,  name="documents"),
    path("profile/documents/delete/<int:pk>/", views.document_delete, name="document-delete"),

    # домашняя
    path("", views.HomeView.as_view(), name="home"),
]

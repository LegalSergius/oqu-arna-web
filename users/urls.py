# users/urls.py

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

    # отправка кода, логин-логаут
    path("send_code/", views.SendCodeToEmailView.as_view(), name="send-code"),
    path("login/",     views.LoginView.as_view(),           name="login"),
    path("logout/",    views.LogoutView.as_view(),          name="logout"),

    # регистрация
    path("registration/",              views.RegistrationView.as_view(),           name="registration"),
    path("verification_code/",         views.VerificationCodeView.as_view(),       name="verification-code"),
    path("registration_set_password/", views.RegistrationSetPasswordView.as_view(), name="register-set-password"),

    # профиль, аватар и документы
    path("profile/",               views.ProfileView.as_view(),     name="profile"),
    path("profile/avatar/",        views.UpdateAvatarView.as_view(), name="update-avatar"),
    path("profile/avatar/delete/", views.DeleteAvatarView.as_view(), name="delete-avatar"),

    # документы пользователя
    path("profile/documents/",               views.DocumentsView.as_view() ,  name="documents"),
    path("profile/documents/delete/<int:pk>/", views.document_delete, name="document-delete"),

    # домашняя
    path("", views.HomeView.as_view(), name="home"),
]
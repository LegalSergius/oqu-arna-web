from django.urls import path
from .views import ActivateUserPasswordResetConfirmView

app_name = 'users'

urlpatterns = [
    path(
        'activate/<uidb64>/<token>/',
        ActivateUserPasswordResetConfirmView.as_view(),
        name='activate'
    ),
]

from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy


class ActivateUserPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('password_reset_complete')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()          # пароль уже сохранён
        user.is_active = True       # активируем
        user.save(update_fields=['is_active'])
        return response

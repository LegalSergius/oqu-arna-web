from django.shortcuts import redirect
from django.urls import reverse

class StaffRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        if user.is_authenticated and user.is_staff and not user.is_superuser:
            # Проверяем, не находится ли пользователь уже на кастомной админке
            if not request.path.startswith('/staff/'):  # замените на нужный префикс
                return redirect(reverse('custom_admin_home'))  # имя вашей кастомной админки

        return self.get_response(request)


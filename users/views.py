from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from smtplib import SMTPRecipientsRefused

from .register_code import generate_code, save_code, get_code, delete_code
from oquArnaWeb import settings

User = get_user_model()

class ActivateUserPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('password_reset_complete')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()          # пароль уже сохранён
        user.is_active = True       # активируем
        user.save(update_fields=['is_active'])
        return response


class SendCodeToEmailView(View):
    def get(self, request):

        email=request.session.get('email')

        code = generate_code()
        save_code(f"register-code:{email}", code)

        request.session['email'] = email

        # email
        title = "Oqu Arna код :)"
        message = f"Ваш код - {code} Никому его не говорите."
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]

        send_mail(title, message, from_email, recipient_list, fail_silently=False)

        after_url = request.session.get('page_to_go_after_sending', 'users:verification-code')

        return redirect(after_url)


class HomeView(View):
    def get(self, request):
        return render(request, 'index.html')

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:

            login(request, user)
            return redirect('users:home')
        else:

            messages.error(request, "Неверный email или пароль")

        return render(request, 'login.html')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('users:login')

class EntryEmailView(View):
    template_name = 'entry_email.html'
    success_url = 'users:send-code'
    page_to_go_after_sending = 'users:verification-code'
    page_to_go_after_confirmation = 'users:reset-password'
    unsuccessful_url = 'users:login'

    def successful(self, request, email, user):
        request.session['email'] = email
        request.session['page_to_go_after_sending'] = self.page_to_go_after_sending
        request.session['page_to_go_after_confirmation'] = self.page_to_go_after_confirmation

        return redirect(self.success_url)


    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email')
        users = User.objects.filter(email=email)

        if users.exists():

            user = users.first()

            response = self.successful(request, email, user)

            if response:
                return response
        else:
            messages.error(request, "Пользователь с данным email не зарегистрирован")

        return render(request, self.template_name)

class VerificationCodeView(View):
    template_name = 'verification_code.html'
    unsuccessful_url = None

    def successful(self, request, key_code, email):
        delete_code(key_code)
        del request.session['email']
        request.session['verified_email'] = email

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        code = request.POST.get('code')

        email = request.session.get('email')


        if email:
            key = f"register-code:{email}"
            cached_code = get_code(key)

            page_to_after_confirmation = request.session.get('page_to_go_after_confirmation', 'reset-password')

            if cached_code:
                if code != cached_code:
                    messages.error(request, "Неверный код")
                else:
                    self.successful(request, key, email)
                    return redirect(page_to_after_confirmation)


        return render(request, self.template_name)

class ResetPasswordView(View):
    template_name = 'reset_password.html'
    success_url = 'users:login'
    unsuccessful_url = 'users:login'

    def successful(self, request, password, email):
        del request.session['verified_email']
        user = User.objects.get(email=email)
        user.set_password(password)
        return user

    def unsuccessful(self, request):
        messages.error(request, "Пароли не совпадают")



    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):

        email = request.session.get('verified_email')

        if not email and self.unsuccessful_url:
            return redirect(self.unsuccessful_url)

        password = request.POST.get('password')
        password_repeat = request.POST.get('password_repeat')

        if password != password_repeat:
            if self.unsuccessful_url:
                return redirect(self.unsuccessful_url)
        else:
            user = self.successful(request, password, email)
            user.save()

            return redirect(self.success_url)

        return render(request, self.template_name)


class RegisterEntryEmailView(EntryEmailView):
    template_name = 'registration_email.html'

    page_to_go_after_sending = 'users:register-verification-code'
    page_to_go_after_confirmation = 'users:register-set-password'

    def successful(self, request, email, user):
        if user and user.is_active:
            messages.error(request, "Пользователь с данным email зарегистрирован")
            return None

        return super().successful(request, email, user)


class RegisterVerificationCodeView(VerificationCodeView):
    template_name = 'registration_code.html'

class RegisterResetPasswordView(ResetPasswordView):
    template_name = 'registration_password.html'

    def successful(self, request, password, email):

        user = super().successful(request, password, email)
        user.is_active = True

        return user


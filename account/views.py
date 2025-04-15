from smtplib import SMTPRecipientsRefused

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from account.register_code import generate_code, save_code, get_code, delete_code
from oquArnaWeb import settings

User = get_user_model()

class HomeView(View):
    def get(self, request):
        return render(request, 'index.html')

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:

            login(request, user)
            return redirect('home')
        else:

            messages.error(request, "Неверный email или пароль")

        return render(request, 'login.html')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        email = request.POST.get('email')

        users = User.objects.filter(username=email)

        if users.exists():
            users_list = list(users)
            user = users_list[0]

            user_email = user.username

            code = generate_code()
            save_code(f"register-code:{user_email}", code)

            request.session['user_email'] = user_email

            #email
            title = "Oqu Arna код :)"
            message = f"Ваш код - {code} Никому его не говорите."
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]

            number_of_email_sent = send_mail(title, message, from_email, recipient_list, fail_silently=False)

            print(number_of_email_sent)

            if number_of_email_sent < 1:
                messages.error(request, "Введенный email не существует")
            else:
                return redirect('register-code')
        else:
            messages.error(request, "Пользователь с данным email не зарегистрирован")

        return render(request, 'register.html')

class RegisterCodeView(View):
    def get(self, request):
        return render(request, 'register_code.html')

    def post(self, request):
        code = request.POST.get('code')

        user_email = request.session.get('user_email')

        if user_email:
            key = f"register-code:{user_email}"
            code_in_cache = get_code(key)

            if code_in_cache:
                if code != code_in_cache:
                    messages.error(request, "Неверный код")
                else:
                    delete_code(key)
                    del request.session['user_email']

                    request.session['verified_email'] = user_email
                    return redirect('register-set-password')


        return render(request, 'register_code.html')

class RegisterSetPasswordView(View):
    def get(self, request):
        return render(request, 'register_set_password.html')

    def post(self, request):

        email = request.session.get('verified_email')

        if not email:
            return redirect('register')

        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, "Пароли не совпадают")
        else:
            del request.session['verified_email']
            user = User.objects.get(username=email)
            user.set_password(password)
            user.save()

            return redirect('login')

        return render(request, 'register_set_password.html')
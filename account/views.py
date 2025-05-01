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

        return redirect('verification-code')


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

class RegistrationView(View):
    def get(self, request):
        return render(request, 'registration_email.html')

    def post(self, request):
        email = request.POST.get('email')

        users = User.objects.filter(username=email)

        if users.exists():
            users_list = list(users)
            user = users_list[0]

            request.session['email'] = email
            #
            # code = generate_code()
            # save_code(f"register-code:{user_email}", code)
            #
            #
            #
            # #email
            # title = "Oqu Arna код :)"
            # message = f"Ваш код - {code} Никому его не говорите."
            # from_email = settings.EMAIL_HOST_USER
            # recipient_list = [email]
            #
            # number_of_email_sent = send_mail(title, message, from_email, recipient_list, fail_silently=False)
            #
            # print(number_of_email_sent)

            # if number_of_email_sent < 1:
            #     messages.error(request, "Введенный email не существует")
            # else:

            request.session['page_to_go_after_confirmation'] = 'register-set-password'

            return redirect('send-code')
        else:
            messages.error(request, "Пользователь с данным email не зарегистрирован")

        return render(request, 'registration_email.html')

class VerificationCodeView(View):
    def get(self, request):
        return render(request, 'registration_code.html')

    def post(self, request):
        code = request.POST.get('code')

        user_email = request.session.get('email')


        if user_email:
            key = f"register-code:{user_email}"
            code_in_cache = get_code(key)

            page_to_after_confirmation = request.session.get('page_to_go_after_confirmation')

            print(page_to_after_confirmation)

            if code_in_cache:
                if code != code_in_cache:
                    messages.error(request, "Неверный код")
                else:
                    delete_code(key)
                    del request.session['email']

                    request.session['verified_email'] = user_email
                    return redirect(page_to_after_confirmation)


        return render(request, 'registration_code.html')

class RegistrationSetPasswordView(View):
    def get(self, request):
        return render(request, 'registration_password.html')

    def post(self, request):

        email = request.session.get('verified_email')

        if not email:
            return redirect('registration')

        password = request.POST.get('password')
        password_repeat = request.POST.get('password_repeat')

        print(password + " " + password_repeat)

        if password != password_repeat:
            messages.error(request, "Пароли не совпадают")
        else:
            del request.session['verified_email']
            user = User.objects.get(username=email)
            user.set_password(password)
            user.save()

            return redirect('login')

        return render(request, 'registration_password.html')
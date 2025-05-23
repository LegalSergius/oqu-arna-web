<<<<<<< Updated upstream
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy
=======
from django.shortcuts import render

from smtplib import SMTPRecipientsRefused
>>>>>>> Stashed changes

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
<<<<<<< Updated upstream
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .forms import DocumentUploadForm
from .models import Document
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import redirect
from django.contrib import messages

from smtplib import SMTPRecipientsRefused

from .register_code import generate_code, save_code, get_code, delete_code


User = get_user_model()

class ActivateUserPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('password_reset_complete')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()          # пароль уже сохранён
        user.is_active = True       # активируем
        user.save(update_fields=['is_active'])
        return response


=======

from .register_code import generate_code, save_code, get_code, delete_code
from oquArnaWeb import settings

User = get_user_model()

>>>>>>> Stashed changes
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

<<<<<<< Updated upstream
        after_url = request.session.get('page_to_go_after_sending', 'users:verification-code')

        return redirect(after_url)

class HomeView(LoginRequiredMixin, View):
=======
        return redirect('verification-code')


class HomeView(View):
>>>>>>> Stashed changes
    def get(self, request):
        return render(request, 'index.html')

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
<<<<<<< Updated upstream

        if user is not None:

            login(request, user)
            return redirect('users:home')
=======
        if user is not None:

            login(request, user)
            return redirect('home')
>>>>>>> Stashed changes
        else:

            messages.error(request, "Неверный email или пароль")

        return render(request, 'login.html')

<<<<<<< Updated upstream
class LogoutView(LoginRequiredMixin, View):
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
=======
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class RegistrationView(View):
    def get(self, request):
        return render(request, 'registration_email.html')
>>>>>>> Stashed changes

    def post(self, request):
        email = request.POST.get('email')

        users = User.objects.filter(email=email)

        if users.exists():
            users_list = list(users)
            user = users_list[0]

<<<<<<< Updated upstream
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
=======
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
>>>>>>> Stashed changes

    def post(self, request):
        code = request.POST.get('code')

<<<<<<< Updated upstream
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
=======
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
>>>>>>> Stashed changes

    def post(self, request):

        email = request.session.get('verified_email')

<<<<<<< Updated upstream
        if not email and self.unsuccessful_url:
            return redirect(self.unsuccessful_url)
=======
        if not email:
            return redirect('registration')
>>>>>>> Stashed changes

        password = request.POST.get('password')
        password_repeat = request.POST.get('password_repeat')

<<<<<<< Updated upstream
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


class   ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'profile.html')

    def post(self, request):
        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')

        request.user.full_name = full_name

        request.user.phone_number = phone_number

        request.user.save()
        return render(request, 'profile.html')


class UpdateAvatarView(LoginRequiredMixin, View):
    """Сохраняет файл в user.avatar"""
    def post(self, request):
        avatar_file = request.FILES.get('avatar')
        if not avatar_file:
            messages.error(request, 'Файл не выбран')
            return redirect('users:profile')

        request.user.avatar = avatar_file
        request.user.save(update_fields=['avatar'])
        messages.success(request, 'Фото профиля обновлено')
        return redirect('users:profile')


class DeleteAvatarView(LoginRequiredMixin, View):
    """Удаляет аватар"""
    def post(self, request):
        if request.user.avatar:
            request.user.avatar.delete(save=False)
            request.user.avatar = None
            request.user.save(update_fields=['avatar'])
            messages.success(request, 'Фото профиля удалено')
        return redirect('users:profile')

@login_required
def document_list(request):

    docs = request.user.documents.all()
    form = DocumentUploadForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        new_doc = form.save(commit=False)
        new_doc.user = request.user
        new_doc.save()
        return redirect('users:documents')

    return render(request, 'documents/list.html', {
        'docs': docs,
        'form': form,
    })


@login_required
def document_delete(request, pk):

    doc = get_object_or_404(Document, pk=pk)
    if doc.user != request.user and not request.user.is_staff:
        return HttpResponseForbidden("Нельзя удалять чужие документы")
    doc.delete()
    return redirect('users:documents')

class DocumentsView(View):
    def get(self, request):
        docs = request.user.documents.all()
        return render(request, 'my_documents.html', {'docs': docs})

    def post(self, request   ):
        docs = request.user.documents.all()
        for file in request.FILES.getlist('files'):
            document = Document()
            document.file = file
            document.user = request.user
            document.title = file.name
            document.save()

        return render(request, 'my_documents.html', {'docs': docs})
=======
        print(password + " " + password_repeat)

        if password != password_repeat:
            messages.error(request, "Пароли не совпадают")
        else:
            del request.session['verified_email']
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()

            return redirect('login')

        return render(request, 'registration_password.html')
>>>>>>> Stashed changes

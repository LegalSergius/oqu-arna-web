from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser
from .forms  import CustomUserCreationForm, CustomUserChangeForm, CustomPasswordResetForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = (
        'email', 'full_name', 'phone_number',
        'organization', 'country', 'city',
        'is_educator', 'is_active', 'is_staff', 'date_joined'
    )
    search_fields = (
        'email', 'full_name', 'phone_number',
        'organization', 'country', 'city'
    )
    ordering = ('email',)
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'is_educator', 'country')

    readonly_fields = ('last_login', 'date_joined')

    fieldsets = (
        (_('Основная информация'), {
            'fields': ('username', 'email', 'password')
        }),
        (_('Личная информация'), {
            'fields': (
                'full_name', 'phone_number', 'organization',
                'country', 'city'
            )
        }),
        (_('Права доступа'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'is_educator', 'groups', 'user_permissions'
            )
        }),
        (_('Важные даты'), {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (_('Регистрация нового пользователя'), {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'full_name', 'phone_number',
                'organization', 'country', 'city', 'is_educator'
            ),
        }),
    )

    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None
        if is_new:
            obj.is_active = False
            obj.set_unusable_password()
        super().save_model(request, obj, form, change)

        if is_new and obj.email:
            reset_form = CustomPasswordResetForm({'email': obj.email})
            if reset_form.is_valid():
                reset_form.save(
                    request=request,
                    use_https=request.is_secure(),
                    email_template_name='registration/invite_email.txt',
                    subject_template_name='registration/invite_subject.txt',
                )
from django.contrib import admin
<<<<<<< Updated upstream
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Document
=======

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

>>>>>>> Stashed changes
from .models import CustomUser
from .forms  import CustomUserCreationForm, CustomUserChangeForm, CustomPasswordResetForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
<<<<<<< Updated upstream
    form = CustomUserChangeForm
    model = CustomUser
=======
    form     = CustomUserChangeForm
    model    = CustomUser
>>>>>>> Stashed changes

    list_display = (
        'email', 'full_name', 'phone_number',
        'organization', 'country', 'city',
<<<<<<< Updated upstream
        'is_educator', 'is_active', 'is_staff', 'date_joined'
=======
        'is_educator', 'is_active', 'is_staff'
>>>>>>> Stashed changes
    )
    search_fields = (
        'email', 'full_name', 'phone_number',
        'organization', 'country', 'city'
    )
    ordering = ('email',)
<<<<<<< Updated upstream
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'is_educator', 'country')

    readonly_fields = ('last_login', 'date_joined')

    fieldsets = (
        (_('Основная информация'), {
            'fields': ('username', 'email', 'password')
        }),
=======

    fieldsets = (
        (None, {'fields': ('email',)}),
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
        (_('Важные даты'), {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (_('Регистрация нового пользователя'), {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'full_name', 'phone_number',
=======
        (_('Важные даты'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'full_name', 'phone_number',
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display  = ('title', 'user', 'uploaded_at')
    search_fields = ('title', 'user__email')
    autocomplete_fields = ('user',)
=======
>>>>>>> Stashed changes

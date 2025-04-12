from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'email', 'full_name', 'phone_number',
            'organization', 'country', 'city', 'is_educator'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'email':
                self.fields[field].required = False


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

class CustomPasswordResetForm(PasswordResetForm):
    def get_users(self, email):
        return CustomUser.objects.filter(email=email)

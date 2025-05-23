from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm
from .models import CustomUser
<<<<<<< Updated upstream
from django import forms
from .models import Document
=======
>>>>>>> Stashed changes


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
<<<<<<< Updated upstream
        return CustomUser.objects.filter(email=email)


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model  = Document
        fields = ('title', 'file')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название PDF документа'
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
        }

    def clean_file(self):
        f = self.cleaned_data['file']
        if f.size > 5 * 1024 * 1024:          # 5 MB
            raise forms.ValidationError('Файл превышает 5 МБ.')
        return f
=======
        return CustomUser.objects.filter(email=email)
>>>>>>> Stashed changes

from django import forms
from unicodedata import category

import common.models
from authors_works.models import AuthorWork, Status
from . import widgets
from .widgets import CustomFileInput


class AuthorWorkForm(forms.ModelForm):
    upload = forms.FileField(required=False, widget=CustomFileInput)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = AuthorWork
        fields = ['name', 'description', 'category', 'status', 'price', 'upload']

        widgets = {
            'name': widgets.InputGroupText(
                text="Название:",
                attrs={
                    "class": "input-group input-info mb-3",
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Описание...',
                    'class': 'input-info input-textarea',
                }
            ),

            'category': widgets.SelectInput(
                text="Категория",

            ),

            'status': widgets.RadioInput,
            'price': widgets.InputGroupText(
                text="Цена:",
                input_type="number",
                default="0",
                attrs={
                    "class": "input-group input-info mt-3",
                    "id": "price"
                }
            ),
        }

    def save(self, commit=True):

        instance = super().save(commit=False)

        uploads_file = self.cleaned_data.get('upload')
        if uploads_file:
            content = common.models.Content()
            content.file_name = uploads_file.name
            content.file.save(uploads_file.name, uploads_file, save=True)
            print(uploads_file)
            instance.file = content

        instance.creator = self.user

        if commit:
            instance.save()

        return instance
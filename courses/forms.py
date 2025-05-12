from django import forms
from common.models import Category, Content
from .models import Course
from datetime import date
# from . import widgets
# from .widgets import CustomFileInput


class CourseForm(forms.ModelForm):
    guideline_upload = forms.FileField(required=True)

    def __init__(self, *args, **kwargs):
        self.creator = kwargs.pop('creator', None)
        super().__init__(*args, **kwargs)

        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].empty_label = '► Выберите категорию'


    class Meta:
        model = Course
        fields = ['name', 'description', 'category', 'participants_count', 'start_date', 'end_date', 'guideline']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'modal-title position-absolute top-25 start-50 translate-middle-x w-75 fs-5 text-center fw-bold border-0',
                    'placeholder': 'Название курса...'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Добавить описание...',
                    'class': 'form-control',
                }
            ),
            'category': forms.Select(
                attrs={
                    'class': 'modalBodyCell modalBodyCellValue bg-white fs-5 text-center fw-bold d-flex justify-content-center align-items-center rounded-4 border-0'
                }
            ),
            'start_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'placeholder': '► Выберите дату',
                    'min': date.today().strftime('%Y-%m-%d'),
                    'class': 'modalBodyCell modalBodyCellValue bg-white fs-5 text-center fw-bold d-flex justify-content-center align-items-center rounded-4 border-0'
                }
            ),
            'end_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'placeholder': '► Выберите дату',
                    'min': date.today().strftime('%Y-%m-%d'),
                    'class': 'modalBodyCell modalBodyCellValue bg-white fs-5 text-center fw-bold d-flex justify-content-center align-items-center rounded-4 border-0'
                }
            ),
            'participants_count': forms.NumberInput(
                attrs={
                    'class': 'modalBodyCell modalBodyCellValue bg-white fs-5 text-center fw-bold d-flex justify-content-center align-items-center rounded-4 border-0'
                }
            ),
            'guideline': forms.ClearableFileInput(
                attrs={
                    'class': 'd-none',
                    'id': 'fileInput'
                }
            )
        }

    def save(self, commit=True):
        instance = super().save(commit=False)

        print(instance)

        uploads_file = self.cleaned_data.get('guideline_upload')

        print(uploads_file)
        if uploads_file:
            content = Content()
            content.file.save(uploads_file.name, uploads_file, save=True)
            print(uploads_file)
            instance.guideline = content

        instance.creator = self.creator

        if commit:
            instance.save()

        return instance
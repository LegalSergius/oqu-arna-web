from django import forms
from common.models import Category, Content
from .models import Course, Lesson
from datetime import date


class CourseForm(forms.ModelForm):
    guideline_upload = forms.FileField(required=True)

    def __init__(self, *args, **kwargs):
        self.creator = kwargs.pop('creator', None)
        super().__init__(*args, **kwargs)

        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].empty_label = '► Выберите категорию'


    class Meta:
        model = Course
        fields = ['name', 'description', 'category', 'participants_count', 'start_date', 'end_date']
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
                    'class': 'modalBodyCell modalBodyCellValue bg-white fs-5 text-center fw-bold d-flex justify-content-center align-items-center rounded-4 border-0',
                    'min': 0
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
            uploaded_file_name = uploads_file.name
            content.file_name = uploaded_file_name

            content.file.save(uploaded_file_name, uploads_file, save=True)
            print(uploads_file)
            instance.guideline = content

        instance.creator = self.creator

        if commit:
            instance.save()

        return instance
    

class LessonForm(forms.ModelForm):
    conference_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'id': 'conferenceURL',
            'type': 'hidden',
            'required': False
        })
    )

    class Meta:
        model = Lesson
        fields = ['name', 'description', 'lesson_date']
        widgets = {
            'name': forms.TextInput(attrs={
                'id': 'lessonNameInput',
                'class': 'form-control fs-3 mb-2 text-center border-0 contentAppThemeColor',
                'style': 'color: var(--primary-color); background: var(--background-page-color);',
                'placeholder': 'Первое занятие',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control w-100 px-3 mx-auto appThemeBorderColor',
                'rows': 4,
                'placeholder': 'Описание занятия',
                'required': True
            }),
            'lesson_date': forms.DateTimeInput(attrs={
                'id': 'datetimeInput',
                'type': 'hidden',
                'required': True
            })
        }
        from django.forms import inlineformset_factory
        from .models import Question, Answer

        QuestionFormSet = inlineformset_factory(
            Lesson, Question, fields=['text'], extra=1, can_delete=True
        )

        AnswerFormSet = inlineformset_factory(
            Question, Answer, fields=['text', 'is_correct'], extra=2, can_delete=True
        )
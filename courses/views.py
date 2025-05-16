from django.http import JsonResponse, Http404, HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from common.views import CategoriesListView, EntitiesListView, file_response
from django.views.generic import View, CreateView, DetailView, ListView
from django.urls import reverse_lazy
from courses.models import Course, Lesson
from common.models import Category, Content
from courses.forms import CourseForm, LessonForm
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from pathlib import Path
import os


class CoursesCategoriesView(CategoriesListView):
    template_name = 'course_category.html'


class CoursesListView(EntitiesListView):
    model = Course
    template_name = 'courses.html'
    context_object_name = 'courses'

    
class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'components/create-modal.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['creator'] = self.request.user

        return kwargs

    def get(self, request, *args, **kwargs):
        if not Category.objects.exists():
            return JsonResponse({'error': 'Нельзя добавить курсы. Не создана ни одна категория курсов. Обратитесь к администратору'}, status=400)
        
        form = self.get_form()
        html = render_to_string(self.template_name, {'form': form}, request=request)

        return JsonResponse({'html': html})
    
    def get_success_url(self):
        return reverse_lazy('courses', kwargs={'category': self.object.category.pk})
    
    def form_valid(self, form):
        self.object = form.save()

        messages.success(self.request, 'Курс успешно создан')

        return HttpResponseRedirect(self.get_success_url())
    

class CourseDetailView(DetailView):
    model = Course
    template_name = 'components/modal.html'
    context_object_name = 'course'
    pk_url_kwarg = 'course_id'


    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            return JsonResponse({'error': 'Курс не найден. Возможно он был удалён'}, status=404)

        course = self.object
        html = render_to_string(self.template_name, {'course': course}, request=request)
        
        output_error_message = None
        try:
            content = course.guideline
        except ObjectDoesNotExist:
            output_error_message = 'У данного курса указан файл, который не существует!'

        data = {
            'html': html,
            'message': output_error_message
        }

        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['file_name'] = self.object.guideline.file_name

        return context
    

class DownloadCourseView(View):
    def get(self, request, content_id):
        try:
            course_content = Content.objects.get(pk=content_id)
        except ObjectDoesNotExist:
            return Http404('Запрашиваемый файл тематики курсов не может быть скачан. Может быть, он был удалён.')
        
        return file_response(course_content)
    

class LessonsListView(ListView):
    model = Lesson
    template_name = 'lessons.html'
    context_object_name = 'lessons'

    def get(self, request, *args, **kwargs):
        course_id = self.kwargs.get('course_id')
        try:
            self.course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            raise Http404('Курс не доступен. Возможно, он был удалён')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.course.lessons.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        context['course_name'] = self.course.name

        return context


class LessonCreateView(CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'lessonActions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_id = self.kwargs.get('course_id')
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            raise Http404('Курс не найден')
        
        context['course_id'] = course.id
        context['course_name'] = course.name
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_educator:
            raise Http404('Нет прав')
        return super().dispatch(request, *args, **kwargs)
    
    def form_invalid(self, form):
        for field, errors in form.errors.items():
            if field == 'lesson_date':
                messages.error(self.request, 'Для добавления занятия нужно определить дату проведения')

        return super().form_invalid(form)
    
    def form_valid(self, form):
        print('Cleaned data - ', form.cleaned_data)

        course_id = self.kwargs.get('course_id')
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            raise Http404('Курс не найден')
    

        form.instance.course = course
        lesson = form.save()

        temp_files = self.request.session.get('temp_files', [])
        for rel_path in temp_files:
            full_temp_path = Path(settings.MEDIA_ROOT) / rel_path
            if not full_temp_path.exists():
                messages.error(self.request, 'Некоторые файлы содержимого занятия были утеряны. Пожалуйста, проверьте в загрузке материалов')
                return render(self.request, self.template_name, {
                    'form': form,
                    'course_id': course.id,
                    'course_name': course.name
                })
            content_filename = full_temp_path.name

            with open(full_temp_path, 'rb') as f:
                content = Content()
                content.file_name = content_filename
                content.file.save(content_filename, File(f), save=True)

            os.remove(full_temp_path)

            lesson.assignments.add(content)  # через связку m2m, если она есть

        self.request.session['temp_files'] = []
        return super().form_valid(form)


    def get_success_url(self):
        return reverse_lazy('lessons', kwargs={'course_id': self.kwargs['course_id']})
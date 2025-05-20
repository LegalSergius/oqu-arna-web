from django.http import JsonResponse, Http404, HttpResponseRedirect, HttpResponseForbidden
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from common.views import CategoriesView, EntitiesListView, file_response
from django.views.generic import View, CreateView, DetailView, ListView
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy
from courses.models import Course, Lesson
from common.models import Category, Content
from courses.forms import CourseForm, LessonForm
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from pathlib import Path
import os
import requests, base64


class CoursesCategoriesView(CategoriesView):
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

    def get_initial(self):
        initial = super().get_initial()
        session_data = self.request.session.get('lesson_form_temp')

        if session_data:
            initial.update(session_data)
        
        return initial

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
        for field, _ in form.errors.items():
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


@require_POST
def save_lesson_temporary(request):
    request.session['lesson_form_temp'] = request.POST.dict()

    return JsonResponse({'status': 'ok'})


def zoom_oauth_start(request):
    token_url = "https://zoom.us/oauth/token"
    
    response = requests.post(
        token_url,
        headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        data={
            'grant_type': 'account_credentials',
            'account_id': settings.ZOOM_ACCOUNT_ID,
        },
        auth=(settings.ZOOM_CLIENT_ID, settings.ZOOM_CLIENT_SECRET)
    )

    print('response - ', response.json()['access_token'])
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'Error getting token: {response.text}')
    

def get_zoom_access_token(request):
    url = "https://zoom.us/oauth/token"
    response = requests.post(
        url,
        params={
            "grant_type": "account_credentials",
            "account_id": settings.ZOOM_ACCOUNT_ID,
        },
        auth=(settings.ZOOM_CLIENT_ID, settings.ZOOM_CLIENT_SECRET)
    )

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(f"Zoom token error: {response.text}")


def create_zoom_meeting(topic, start_time, duration_minutes):
    token = get_zoom_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    body = {
        "topic": topic,
        "type": 2,  # Запланированная встреча
        "start_time": start_time,  # в формате "2025-05-13T15:00:00Z"
        "duration": duration_minutes,
        "timezone": "Europe/Moscow",
        "settings": {
            "join_before_host": True,
            "approval_type": 0,
            "registration_type": 1,
            "audio": "both",
            "auto_recording": "cloud"
        }
    }

    response = requests.post("https://api.zoom.us/v2/users/me/meetings", headers=headers, json=body)

    if response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Zoom meeting creation error: {response.text}")


class CreateZoomMeetingView(View):
    def get(self, request):
        if not request.user.is_authenticated or not request.user.is_educator:
            return HttpResponseForbidden('Нет прав')

        access_token = request.GET.get('access_token')
        meeting_info = create_zoom_meeting(access_token)
        return JsonResponse(meeting_info)
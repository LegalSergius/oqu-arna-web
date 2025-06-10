# courses/views.py

import tempfile
import zipfile
from collections import OrderedDict
from multiprocessing.reduction import send_handle

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, Http404, HttpResponseRedirect, HttpResponseForbidden, FileResponse
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View, CreateView, DetailView, ListView, TemplateView, UpdateView
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Min, Max
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from pathlib import Path
from datetime import datetime, time, timedelta
from json import loads
import os, requests

from courses import models
from courses.models import Course, Lesson, Conference, Test, Question, Answer
from courses.forms import CourseForm, LessonForm, QuestionFormSet, AnswerFormSet
from courses.utils import get_zoom_access_token
from common.models import Category, Content
from common.views import CategoriesView, EntitiesListView, file_response

User = get_user_model()


def file_response_zip(request, lesson):
    contents = lesson.assignments.all()
    if not contents.exists():
        messages.error(request, 'У этого урока нету материалов')
        return

    temp_file = tempfile.TemporaryFile()
    cont = None
    with zipfile.ZipFile(temp_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for content in contents:
            cont = content
            arcname = os.path.basename(content.file_name)
            zf.write(content.file.path, arcname=arcname)

    temp_file.seek(0)

    return FileResponse(
        temp_file,
        as_attachment=True,
        filename=cont.file_name,
        content_type='application/zip',
    )


DAYS_RU = [
    'понедельник', 'вторник', 'среда',
    'четверг', 'пятница', 'суббота'
]


def _blank_slot(day_date: datetime, start_at: time) -> dict:
    end_at = (datetime.combine(day_date, start_at) +
              timedelta(minutes=50)).time()
    return {'start': start_at, 'end': end_at, 'title': ''}


def _fill_to_seven(day_date: datetime, day_items: list[dict]) -> list[dict]:
    while len(day_items) < 7:
        if day_items:
            last_end = day_items[-1]['end']
            if last_end.hour >= 23:
                last_end = time(0, 0)
            next_start = time(last_end.hour + 1, 0)
        else:
            next_start = time(8, 0)
        day_items.append(_blank_slot(day_date, next_start))
    return day_items


def build_week_schedule(*, week_index: int | None = None, first_date, last_date, filters=dict()) -> list[dict]:
    total_weeks = ((last_date - first_date).days // 7) + 1
    if week_index is None:
        week_index = total_weeks

    week0_monday = first_date - timedelta(days=first_date.weekday())
    monday = week0_monday + timedelta(weeks=week_index)
    sunday = monday + timedelta(days=6)

    filters['lesson_date__range'] = (monday, sunday)
    week_lessons = Lesson.objects.filter(**filters).order_by('lesson_date')

    schedule: list[dict] = []
    for i, day_ru in enumerate(DAYS_RU):
        day_date = monday + timedelta(days=i)
        day_qs = [l for l in week_lessons if l.lesson_date.weekday() == i]
        day_items: list[dict] = []
        for les in day_qs:
            start_at = les.lesson_date.time()
            end_at = (les.lesson_date + les.duration).time()
            day_items.append({'start': start_at, 'end': end_at, 'title': les.course.name})
        schedule.append({day_ru: _fill_to_seven(day_date, day_items)})
    return schedule


def add_lesson_stat(conference, test, task, comment):
    return {
        'conference': conference,
        'test': test,
        'task': task,
        'comment': comment,
    }


def lesson_add_files(request, lesson, form, course, template_name):
    temp_files = request.session.get('temp_files', [])
    for rel_path in temp_files:
        full_temp_path = Path(settings.MEDIA_ROOT) / rel_path
        if not full_temp_path.exists():
            messages.error(request,
                           'Некоторые файлы содержимого занятия были утеряны. Пожалуйста, проверьте в загрузке материалов')
            return render(request, template_name, {
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
        lesson.assignments.add(content)


# --------------------------------------------------------------------

class CoursesCategoriesView(LoginRequiredMixin, CategoriesView):
    template_name = 'course_category.html'


class CoursesListView(LoginRequiredMixin, EntitiesListView):
    model = Course
    template_name = 'courses.html'
    context_object_name = 'courses'

    def get_personal_entities(self):
        personal_works = bool(self.request.GET.get('personal_works'))
        user = self.request.user
        filter = {}
        if personal_works:
            if user.is_educator:
                filter['creator'] = user
            else:
                filter['participants'] = user
        return filter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        courses = context['courses']
        for course in courses:
            if self.request.user.is_educator:
                course.is_access = (course.creator == self.request.user)
            else:
                course.is_access = course.participants.filter(pk=self.request.user.pk).exists()
        context['courses'] = courses
        return context


class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'components/create-modal.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['creator'] = self.request.user
        return kwargs

    def get(self, request, *args, **kwargs):
        if not Category.objects.exists():
            return JsonResponse(
                {'error': 'Нельзя добавить курсы. Не создана ни одна категория курсов. Обратитесь к администратору'},
                status=400
            )
        form = self.get_form()
        html = render_to_string(self.template_name, {'form': form}, request=request)
        return JsonResponse({'html': html})

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, 'Курс успешно создан')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('courses', kwargs={'category': self.object.category.pk})


class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'components/modal.html'
    context_object_name = 'course'
    pk_url_kwarg = 'course_id'

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            return JsonResponse({'error': 'Курс не найден. Возможно он был удалён'}, status=404)
        html = render_to_string(self.template_name, {'course': self.object}, request=request)
        output_error_message = None
        try:
            _ = self.object.guideline
        except ObjectDoesNotExist:
            output_error_message = 'У данного курса указан файл, который не существует!'
        return JsonResponse({'html': html, 'message': output_error_message})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['file_name'] = self.object.guideline.file_name
        return context


class DownloadCourseView(LoginRequiredMixin, View):
    def get(self, request, content_id):
        try:
            course_content = Content.objects.get(pk=content_id)
        except ObjectDoesNotExist:
            raise Http404('Запрашиваемый файл тематики курсов не может быть скачан. Может быть, он был удалён.')
        return file_response(course_content)


class DownloadTaskView(LoginRequiredMixin, View):
    def get(self, request, lesson_id):
        lesson = Lesson.objects.get(pk=lesson_id)
        if lesson.course.participants.filter(pk=self.request.user.pk).exists():
            response = file_response_zip(request, lesson)
            if response:
                return response
        return redirect('lessons-student-list', course_id=lesson.course.id)


class LessonsListView(LoginRequiredMixin, ListView):
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
        context['course'] = self.course
        return context


class LessonsStudentListView(LessonsListView):
    template_name = 'course_detail.html'


class LessonCreateView(LoginRequiredMixin, CreateView):
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
        course = Course.objects.get(pk=course_id)
        self.request.session['page_redirect'] = {
            'url_name': 'create-lesson',
            'kwargs': {'course_id': course_id}
        }
        context.update({
            'course_id': course.id,
            'course_name': course.name
        })
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_educator:
            raise Http404('Нет прав')
        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        if 'lesson_date' in form.errors:
            messages.error(self.request, 'Для добавления занятия нужно определить дату проведения')
        return super().form_invalid(form)

    def form_valid(self, form):
        course = Course.objects.get(pk=self.kwargs.get('course_id'))
        form.instance.course = course
        lesson = form.save()
        response = lesson_add_files(self.request, lesson, form, course, self.template_name)
        if response:
            return response
        conference_url = form.cleaned_data.get('conference_url')
        if conference_url:
            Conference.objects.create(zoom_id=conference_url, lesson=lesson)
        self.request.session['temp_files'] = []
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('lessons', kwargs={'course_id': self.kwargs['course_id']})


class LessonUpdateView(LoginRequiredMixin, UpdateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'edit_lesson.html'
    pk_url_kwarg = 'lesson_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson = Lesson.objects.get(pk=self.kwargs.get('lesson_id'))
        self.request.session['page_redirect'] = {
            'url_name': 'lessons-update',
            'kwargs': {'lesson_id': lesson.id}
        }
        context.update({
            'course_id': lesson.course.id,
            'course_name': lesson.course.name
        })
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_educator:
            raise Http404('Нет прав')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        lesson = Lesson.objects.get(pk=self.kwargs.get('lesson_id'))
        course = lesson.course
        response = lesson_add_files(self.request, lesson, form, course, self.template_name)
        if response:
            return response
        self.request.session['temp_files'] = []
        return super().form_valid(form)

    def get_success_url(self):
        lesson = Lesson.objects.get(pk=self.kwargs.get('lesson_id'))
        return reverse_lazy('lessons', kwargs={'course_id': lesson.course.id})


class LessonStatisticView(LoginRequiredMixin, TemplateView):
    template_name = 'lessonStats.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_educator:
            raise Http404('Нет прав')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        lesson = Lesson.objects.get(pk=self.kwargs.get('lesson_id'))
        course = lesson.course
        users = course.participants.all()
        lesson_statistics = lesson.lesson_statics.all()
        statistics = []
        for idx, user in enumerate(users, start=1):
            data = {'i': idx, 'user': user}
            stat_qs = lesson_statistics.filter(user=user)
            if stat_qs.exists():
                stat = stat_qs.first()
                data.update(add_lesson_stat(stat.conference, stat.test, stat.task, stat.comment))
            else:
                data.update(add_lesson_stat('-', '-', '-', ''))
            statistics.append(data)
        return {'lesson': lesson, 'statistics': statistics, 'course': course}

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):
        lesson = Lesson.objects.get(pk=self.kwargs.get('lesson_id'))
        user = User.objects.get(pk=request.POST.get('user-pk'))
        conference = bool(request.POST.get('conference'))
        test = bool(request.POST.get('test'))
        task = bool(request.POST.get('task'))
        comment = request.POST.get('comment')
        stat_qs = lesson.lesson_statics.filter(user=user)
        if stat_qs.exists():
            stat = stat_qs.first()
            stat.conference = conference
            stat.test = test
            stat.task = task
            stat.comment = comment
            stat.save()
        else:
            new_stat = models.LessonStatistics.objects.create(
                user=user, conference=conference, test=test, task=task, comment=comment
            )
            lesson.lesson_statics.add(new_stat)
        return self.render_to_response(self.get_context_data(**kwargs))


class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = 'lessons_detail.html'
    context_object_name = 'lesson'
    pk_url_kwarg = 'lesson_id'


class ScheduleView(LoginRequiredMixin, TemplateView):
    template_name = 'schedule.html'

    def get_context_data(self, **kwargs):
        filters = {}
        if self.request.user.is_educator:
            filters['course__creator'] = self.request.user
        else:
            filters['course__participants'] = self.request.user

        if not Lesson.objects.filter(**filters).exists():
            return {}

        borders = Lesson.objects.filter(**filters).aggregate(first=Min('lesson_date'), last=Max('lesson_date'))
        first_date, last_date = borders['first'], borders['last']
        now = timezone.now()

        if first_date.date() >= now.date():
            first_date = now

        options = []
        d = first_date - timedelta(days=first_date.weekday())
        while d <= last_date:
            next_day = d + timedelta(days=6)
            week_index = ((d - first_date).days // 7)
            options.append((f"{d.day}.{d.month:02d} - {next_day.day}.{next_day.month:02d}", week_index))
            d += timedelta(days=7)

        now_week_index = ((last_date - first_date).days // 7)
        week_param = self.request.GET.get('weeks')
        selected = int(week_param) if week_param is not None else now_week_index

        schedule = build_week_schedule(
            week_index=selected,
            first_date=first_date,
            last_date=last_date,
            filters=filters
        )

        sd = [(next(iter(day)), next(iter(day.values()))) for day in schedule]
        return {
            'schedule': sd,
            'options': options,
            'selected_week': selected
        }

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))


@require_POST
def save_lesson_temporary(request):
    request.session['lesson_form_temp'] = request.POST.dict()
    return JsonResponse({'status': 'ok'})


def save_session(request, form_data):
    request.session['lesson_form_temp'] = form_data


def zoom_oauth_start(request):
    token_url = "https://zoom.us/oauth/token"
    response = requests.post(
        token_url,
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        data={'grant_type': 'account_credentials', 'account_id': settings.ZOOM_ACCOUNT_ID},
        auth=(settings.ZOOM_CLIENT_ID, settings.ZOOM_CLIENT_SECRET)
    )
    if response.status_code == 200:
        return response.json()
    raise Exception(f'Error getting token: {response.text}')


def create_zoom_meeting(access_token, lesson_name, lesson_date):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    body = {
        "topic": lesson_name,
        "type": 2,
        "start_time": lesson_date,
        "duration": 60,
        "timezone": "Europe/Moscow",
        "settings": {
            "join_before_host": True,
            "approval_type": 0,
            "registration_type": 1,
            "audio": "both",
            "auto_recording": "cloud"
        }
    }
    resp = requests.post("https://api.zoom.us/v2/users/me/meetings", headers=headers, json=body)
    if resp.status_code == 201:
        return resp.json()
    return JsonResponse({'error': 'Проблема при обработке создания '})


class CreateZoomMeetingView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_educator:
            raise Http404('Нет прав на создание конференций для занятий')
        try:
            data = loads(request.body)
        except Exception:
            return JsonResponse({'error': 'Ошибка обработки входных данных'}, status=400)

        lesson_name = data.get('lesson_name')
        lesson_date = data.get('lesson_date')
        if not lesson_name or not lesson_date:
            return JsonResponse({'error': 'Недостаточно входных данных'}, status=400)
        try:
            access_token = get_zoom_access_token()
        except:
            return JsonResponse({'error': 'Ошибка проверки токена'}, status=400)

        try:
            meeting_info = create_zoom_meeting(access_token, lesson_name, lesson_date)
            meeting_url = meeting_info['join_url']
        except Exception:
            return JsonResponse({'error': 'Ошибка создания конференции'}, status=400)

        return JsonResponse({'meeting_url': meeting_url, 'success': 'Конференция успешно добавлена!'})


class LessonTestCreateView(LoginRequiredMixin, View):
    template_name = 'lesson_test_create.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_educator:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, lesson_id):
        lesson = Lesson.objects.get(pk=lesson_id)
        if lesson.course.creator != request.user:
            return HttpResponseForbidden()

        question_formset = QuestionFormSet(instance=lesson)
        answer_formsets = {
            f'q{form.prefix}': AnswerFormSet(prefix=f'ans-{form.prefix}', instance=form.instance)
            for form in question_formset.forms
        }

        return render(request, self.template_name, {
            'lesson': lesson,
            'question_formset': question_formset,
            'answer_formsets': answer_formsets
        })

    def post(self, request, lesson_id):
        lesson = Lesson.objects.get(pk=lesson_id)
        if lesson.course.creator != request.user:
            return HttpResponseForbidden()

        question_formset = QuestionFormSet(request.POST, instance=lesson)
        answer_formsets = {}

        if question_formset.is_valid():
            questions = question_formset.save(commit=False)
            for q in questions:
                q.lesson = lesson
                q.save()

            for form in question_formset.forms:
                prefix = form.prefix
                answer_formset = AnswerFormSet(
                    request.POST, prefix=f'ans-{prefix}', instance=form.instance
                )
                answer_formsets[prefix] = answer_formset
                if answer_formset.is_valid():
                    answers = answer_formset.save(commit=False)
                    for a in answers:
                        a.question = form.instance
                        a.save()

            messages.success(request, "Вопросы и ответы сохранены.")
            return redirect('lessons', course_id=lesson.course.id)

        # if invalid, re-render with errors
        for form in question_formset.forms:
            prefix = form.prefix
            answer_formsets[prefix] = AnswerFormSet(
                request.POST, prefix=f'ans-{prefix}', instance=form.instance
            )

        return render(request, self.template_name, {
            'lesson': lesson,
            'question_formset': question_formset,
            'answer_formsets': answer_formsets
        })

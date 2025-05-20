import tempfile
import zipfile
from collections import OrderedDict
from multiprocessing.reduction import send_handle

from django.contrib.auth import get_user_model
from django.http import JsonResponse, Http404, HttpResponseRedirect, FileResponse
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic.edit import FormMixin

from common.views import CategoriesView, EntitiesListView, file_response
from django.views.generic import View, CreateView, DetailView, ListView, TemplateView, UpdateView, RedirectView
from django.urls import reverse_lazy

from courses import models
from courses.models import Course, Lesson
from common.models import Category, Content
from courses.forms import CourseForm, LessonForm
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from pathlib import Path
import os

User = get_user_model()

# utils/schedule.py
from datetime import datetime, time, timedelta

from django.utils import timezone
from django.db.models import Min, Max

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
            print(content)
            arcname = os.path.basename(content.file_name)
            zf.write(content.file.path, arcname=arcname)

    print(cont)

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
    """Возвращает «пустое» занятие c длительностью 50 минут."""
    end_at = (datetime.combine(day_date, start_at) +
              timedelta(minutes=50)).time()
    return {'start': start_at, 'end': end_at, 'title': ''}


def _fill_to_seven(day_date: datetime, day_items: list[dict]) -> list[dict]:
    """Добавляет пустые слоты, пока не станет 7 уроков."""
    while len(day_items) < 7:
        if day_items:
            last_end = day_items[-1]['end']
            next_start = time(last_end.hour + 1, 0)
        else:
            next_start = time(8, 0)           # первая пара, если день пуст
        day_items.append(_blank_slot(day_date, next_start))
    return day_items


def build_week_schedule(*, week_index: int | None = None, first_date, last_date, filters=dict()) -> list[dict]:

    # номер запрашиваемой недели

    total_weeks = ((last_date - first_date).days // 7) + 1
    if week_index is None:
        week_index = total_weeks

    # понедельник нужной недели
    week0_monday = first_date - timedelta(days=first_date.weekday())
    monday = week0_monday + timedelta(weeks=week_index)
    sunday = monday + timedelta(days=6)

    # все занятия этой недели
    filters['lesson_date__range'] = (monday, sunday)

    print("create sh:", week0_monday, monday, sunday, week_index)

    week_lessons = (Lesson.objects.filter(**filters).order_by('lesson_date') )

    #print(week_lessons, filters['lesson_date__range'])

    # распределяем по дням
    schedule: list[dict] = []
    for i, day_ru in enumerate(DAYS_RU):
        day_date = monday + timedelta(days=i)
        day_qs = [l for l in week_lessons if l.lesson_date.weekday() == i]

        day_items: list[dict] = []
        for les in day_qs:
            start_at = les.lesson_date.time()
            end_at = (les.lesson_date + les.duration).time()
            day_items.append({'start': start_at, 'end': end_at, 'title': les.course.name})

        #print(day_items)
        schedule.append({day_ru: _fill_to_seven(day_date, day_items)})

    return schedule

def add_lesson_stat(conference, test, task, comment):
    statistic = {}
    statistic['conference'] = conference
    statistic['test'] = test
    statistic['task'] = task
    statistic['comment'] = comment

    return statistic


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

#--------------------------------------------------------------------

class CoursesCategoriesView(CategoriesView):
    template_name = 'course_category.html'


class CoursesListView(EntitiesListView):
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
        context = super(CoursesListView, self).get_context_data(**kwargs)

        courses = context['courses']

        for course in courses:
            is_access = False
            if self.request.user.is_educator:
                is_access = course.creator == self.request.user
            else:
                is_access = course.participants.filter(pk=self.request.user.pk).exists()

            course.is_access = is_access

        context['courses'] = courses

        return context


    
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

class DownloadTaskView(View):
    def get(self, request, lesson_id):
        lesson = Lesson.objects.get(pk=lesson_id)
        if lesson.course.participants.filter(pk=self.request.user.pk).exists():
            response = file_response_zip(request, lesson)

            if response:
                return response

        return redirect('lessons-student-list', course_id=lesson.course.id)

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

        context['course'] = self.course

        return context

class LessonsStudentListView(LessonsListView):
    template_name = 'course_detail.html'

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

        self.request.session['page_redirect'] = {'url_name': 'create-lesson', 'kwargs': {'course_id': course_id}}
        
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

        response = lesson_add_files(self.request, lesson, form, course, self.template_name)

        if response:
            return response

        self.request.session['temp_files'] = []
        return super().form_valid(form)


    def get_success_url(self):
        return reverse_lazy('lessons', kwargs={'course_id': self.kwargs['course_id']})


class LessonUpdateView(UpdateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'edit_lesson.html'
    pk_url_kwarg = 'lesson_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson_id = self.kwargs.get('lesson_id')

        try:
            lesson = Lesson.objects.get(pk=lesson_id)
        except Lesson.DoesNotExist:
            raise Http404('Урок не найден')

        course = lesson.course

        self.request.session['page_redirect'] = {'url_name': 'lessons-update', 'kwargs': {'lesson_id': lesson_id}}

        context['course_id'] = course.id
        context['course_name'] = course.name
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_educator:
            raise Http404('Нет прав')
        return super().dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        lesson_id = self.kwargs.get('lesson_id')

        try:
            lesson = Lesson.objects.get(pk=lesson_id)
        except Lesson.DoesNotExist:
            raise Http404('Урок не найден')

        course = lesson.course

        response = lesson_add_files(self.request, lesson, form, course, self.template_name)

        if response:
            return response

        self.request.session['temp_files'] = []
        return super().form_valid(form)

    def get_success_url(self):
        lesson_id = self.kwargs.get('lesson_id')
        lesson = Lesson.objects.get(pk=lesson_id)

        return reverse_lazy('lessons', kwargs={'course_id': lesson.course.id})

class LessonStatisticView(TemplateView):
    template_name = 'lessonStats.html'

    def get_context_data(self, **kwargs):
        lesson_id = self.kwargs.get('lesson_id')

        lesson = Lesson.objects.get(pk=lesson_id)

        course = lesson.course

        users = lesson.course.participants.all()
        lesson_statistics = lesson.lesson_statics.all()

        statistics = list()

        for i in range(users.count()):
            user = users[i]
            statistics.append({'i': i+1, 'user': user})
            lesson_statistic = lesson_statistics.filter(user=user)

            if lesson_statistic.exists():
                lesson_statistic = lesson_statistic.first()
                stat = add_lesson_stat(lesson_statistic.conference, lesson_statistic.test, lesson_statistic.task, lesson_statistic.comment)
                statistics[i].update(stat)
            else:
                stat = add_lesson_stat('-', '-', '-', '')
                statistics[i].update(stat)

        context = {'lesson': lesson, 'statistics': statistics, 'course': course}
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_educator:
            raise Http404('Нет прав')
        return super().dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):

        return self.render_to_response(self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):

        lesson_id = self.kwargs.get('lesson_id')
        lesson = Lesson.objects.get(pk=lesson_id)

        user_id = request.POST.get('user-pk')
        print(user_id)
        user = User.objects.get(pk=user_id)

        conference = bool(request.POST.get('conference'))
        test = bool(request.POST.get('test'))
        task = bool(request.POST.get('task'))

        comment = request.POST.get('comment')

        lesson_stat = lesson.lesson_statics.filter(user=user)

        if lesson_stat.exists():
            lesson_stat = lesson_stat.first()
            lesson_stat.conference = conference
            lesson_stat.test = test
            lesson_stat.task = task
            lesson_stat.comment = comment
            lesson_stat.save()
        else:
            new_lesson_stat = models.LessonStatistics()
            new_lesson_stat.user = user
            new_lesson_stat.conference = conference
            new_lesson_stat.test = test
            new_lesson_stat.task = task
            new_lesson_stat.comment = comment
            new_lesson_stat.save()
            lesson.lesson_statics.add(new_lesson_stat)

        return self.render_to_response(self.get_context_data(**kwargs))


class LessonDetailView(DetailView):
    model = Lesson
    template_name = 'lessons_detail.html'
    context_object_name = 'lesson'
    pk_url_kwarg = 'lesson_id'



class ScheduleView(TemplateView):
    template_name = 'schedule.html'   # ваш готовый шаблон

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        filters = {}

        if self.request.user.is_educator:
            filters['course__creator'] = self.request.user
        else:
            filters['course__participants'] = self.request.user

        if not Lesson.objects.filter(**filters).exists():
            return {}

        borders = Lesson.objects.filter(**filters).aggregate(
            first=Min('lesson_date'), last=Max('lesson_date')
        )

        first_date: datetime = borders['first']
        last_date: datetime = borders['last']

        now = timezone.now()

        if first_date.date() >= now.date():
            print("true",)
            first_date = now
        print("sfadsfadsfadsfads:", first_date.date(), now.date())
        options = []

        d = first_date - timedelta(days=first_date.weekday())
        print('d:', d)
        while d <= last_date:

            next_day = d + timedelta(days=6)

            week_index = ((d - first_date).days // 7)
            options.append((f"{d.day}.{d.month:02d} - {next_day.day}.{next_day.month:02d}", week_index))
            d += timedelta(days=7)

        now_week_index = ((last_date - first_date).days // 7)

        week_index = kwargs.pop('week')

        if week_index is None:
            week_index = now_week_index
        else:
            week_index = int(week_index)

        schedule = build_week_schedule(week_index=week_index, first_date=first_date, last_date=last_date, filters=filters)

        sd = []

        for day in schedule:
            sd.append((next(iter(day)), next(iter(day.values()))))

        ctx['schedule'] = sd
        ctx['options'] = options
        ctx['selected_week'] = week_index

        return ctx

    def get(self, request, *args, **kwargs):

        week = request.GET.get('weeks', None)

        context = self.get_context_data(**kwargs, week=week)

        return self.render_to_response(context)
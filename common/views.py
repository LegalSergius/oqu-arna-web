from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import Http404, FileResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, View
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from common.models import Category
from courses.models import Course
from pathlib import Path
import os, uuid

# Create your views here.
class CategoriesListView(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'category.html'

    def get_queryset(self):
        kw = {}

        search = self.request.GET.get('search')

        if search:
            kw['name__iregex'] = search

        queryset = self.model.objects.filter(**kw)
        return queryset


class EntitiesListView(ListView):
    def get_queryset(self):
        category_id = self.kwargs.get('category')
        try:
            self.selected_category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            raise Http404('Запрашиваемая категория не была добавлена. Обратитесь к администратору')

        search = self.request.GET.get('search')

        personal_works = bool(self.request.GET.get('personal_works'))

        kw = {
            'category' : self.selected_category,
        }

        if search:
            kw['name__iregex'] = search

        if personal_works:
            kw['creator'] = self.request.user

        queryset = self.model.objects.filter(**kw)
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['category_name'] = self.selected_category.name

        if not is_personal_works(self.request):
            context['active_table_name'] = "one_table"
        else:
            context['active_table_name'] = "two_table"

        return context


class LessonContentView(View):
    template_name = 'content.html'

    def get(self, request, course_id):
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            raise Http404('Курс не доступен. Возможно, он был удалён')

        if not Course.objects.filter(pk=course_id).exists():
            raise Http404('Нельзя добавить содержимое занятия на несуществующий курс. Возможно, он был удалён')

        temporary_files = request.session.get('content_files', [])

        return render(request, self.template_name, {
            'uploaded_files': temporary_files,
            'course_name': course.name,
            'course_id': course.id
        })

    def post(self, request, course_id):
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            raise Http404('Нельзя добавить содержимое занятия на несуществующий курс. Возможно, он был удалён')

        uploaded_files = request.FILES.getlist('content')
        temporary_files = request.session.get('content_files', [])
        if not uploaded_files:
            messages.error(request, 'Добавьте как минимум один файл содержимого')

            return render(request, self.template_name, {
                'uploaded_files': temporary_files,
                'course_id': course.id,
                'course_name': course.name
        })

        tmp_dir = Path(settings.MEDIA_ROOT) / 'tmp'
        tmp_dir.mkdir(parents=True, exist_ok=True)

        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'tmp'))

        for uploaded_file in uploaded_files:
            filename = f"{uuid.uuid4()}_{uploaded_file.name}"
            temp_path = os.path.join('tmp', filename)
            fs.save(filename, uploaded_file)

            temporary_files.append(temp_path)
        
        request.session['temp_files'] = temporary_files
        request.session.modified = True

        messages.success(request, 'Файлы содержимого сохранены')

        return redirect(reverse_lazy('create-lesson', kwargs={'course_id': course_id}))


def is_personal_works(request):
    personal_works = bool(request.GET.get('personal_works'))

    return personal_works


def file_response(content):
    path = content.file.path

    return FileResponse(
        open(path, 'rb'),
        as_attachment=True,
        filename=content.file_name
    )

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
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

User = get_user_model()




class SearchView(ListView):
    field_for_filtering = ''

    def get_filter_parameter(self):
        kwargs = {}

        search = self.request.GET.get('search')

        if search:
            kwargs[f'{self.field_for_filtering}__iregex'] = search

        return kwargs

    def get_queryset(self):
        kw = self.get_filter_parameter()
        queryset = self.model.objects.filter(**kw)
        return queryset

class CategoriesView(SearchView):
    model = Category
    context_object_name = 'categories'
    field_for_filtering = 'name'


class EntitiesListView(LoginRequiredMixin, SearchView):
    field_for_filtering = 'name'

    def get_personal_entities(self):
        personal_works = bool(self.request.GET.get('personal_works'))

        user = self.request.user

        filter = {'creator' : user}

        return filter


    def get_filter_parameter(self):
            kwargs = super().get_filter_parameter()
            category = self.kwargs.get('category')
            try:
                selected_category = Category.objects.get(pk=category)
            except Category.DoesNotExist:
                raise Http404('Запрашиваемая категория не была добавлена. Обратитесь к администратору')

            kwargs['category_id'] = selected_category

            kwargs.update(self.get_personal_entities())

            return kwargs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.kwargs.get('category')

        self.request.session['selected_category'] = category

        context['category'] = category

        if not is_personal_works(self.request):
            context['active_table_name'] = "one_table"
        else:
            context['active_table_name'] = "two_table"

        return context


class LessonContentView(LoginRequiredMixin, View):
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

        page_redirect = self.request.session['page_redirect']

        return redirect(reverse_lazy(page_redirect['url_name'], kwargs=page_redirect['kwargs']))


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

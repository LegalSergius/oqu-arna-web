from django.http import JsonResponse, Http404, HttpResponseRedirect
from django.contrib import messages
from common.views import CategoriesListView, EntitiesListView
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from courses.models import Course
from common.models import Category
from courses.forms import CourseForm
from django.template.loader import render_to_string


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
        return reverse_lazy('courses', kwargs={'pk': self.object.category.pk})
    
    def form_valid(self, form):
        print('files', self.request.FILES)

        # response = super().form_valid(form)
        self.object = form.save()

        messages.success(self.request, 'Курс успешно создан')

        return HttpResponseRedirect(self.get_success_url())

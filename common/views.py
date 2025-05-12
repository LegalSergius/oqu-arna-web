from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.generic import ListView
from common.models import Category

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


def is_personal_works(request):
    personal_works = bool(request.GET.get('personal_works'))

    return personal_works

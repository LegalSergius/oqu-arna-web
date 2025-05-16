from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView

from common import models

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
    model = models.Category
    context_object_name = 'categories'
    field_for_filtering = 'name'

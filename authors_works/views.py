from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from . import models

import common.models

class TestView(View):
    def get(self, request):
        return render(request, 'category.html')

class CategoriesListView(ListView):
    model = common.models.Category
    template_name = "category.html"
    context_object_name = "categories"

class AuthorWorksListView(ListView):
    model = models.AuthorWork
    template_name = 'author_works.html'
    context_object_name = "works"

    def get_queryset(self):
        category_id = self.kwargs.get('category')
        queryset = models.AuthorWork.objects.filter(category_id=category_id)
        return queryset
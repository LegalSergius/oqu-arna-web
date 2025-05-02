from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from authors_works.models import AuthorWork

class TestView(View):
    def get(self, request):
        return render(request, 'category.html')

class CategoriesListView(ListView):
    model = models.Category
    template_name = "category.html"
    context_object_name = "categories"

class AuthorWorksListView(ListView):
    model = AuthorWork
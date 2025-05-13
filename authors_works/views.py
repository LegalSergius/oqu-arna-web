import os
from traceback import print_tb

from django.http import FileResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

from django.views import View
from django.views.generic import ListView, DetailView, CreateView

from common.views import SearchView, CategoriesView

from . import models, forms

import common.models
from .models import Status


#---------------------------------------


def is_personal_works(request):
    personal_works = bool(request.GET.get('personal_works'))

    return personal_works


def file_response(request, author_work):
    content = author_work.file
    path = content.file.path

    return FileResponse(
        open(path, 'rb'),
        as_attachment=True,
        filename=content.file_name
    )



#---------------------------------------





class TestView(View):
    def get(self, request):
        return render(request, 'category.html')

class CategoriesAuthorWorksView(CategoriesView):
    template_name = 'category.html'

class AuthorWorksListView(SearchView):
    model = models.AuthorWork
    template_name = 'author_works.html'
    context_object_name = 'works'
    field_for_filtering = 'name'

    def get_kwargs(self):
        kwargs = super().get_kwargs()

        category = self.kwargs.get('category')
        personal_works = bool(self.request.GET.get('personal_works'))

        kwargs['category_id'] = category

        if personal_works:
            kwargs['creator'] = self.request.user

        return kwargs

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['category'] = self.kwargs['category']

        if not is_personal_works(self.request):
            context['active_table_name'] = "one_table"
        else:
            context['active_table_name'] = "two_table"

        return context

class AuthorWorkDetailView(DetailView):
    model = models.AuthorWork
    template_name = 'author_works_download.html'
    context_object_name = 'work'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        is_acceptable_user = self.object.acceptable_users.filter(pk=user.pk).exists()

        if is_acceptable_user:
            context['is_acceptable_user'] = True

        context['file_name'] = self.object.file.file_name

        return context

class DownloadAuthorWorkView(View):
    def get(self, request, author_work_id):
        author_work = models.AuthorWork.objects.get(pk=author_work_id)

        if author_work.status == Status.private:
            is_acceptable_user = author_work.acceptable_users.filter(pk=request.user.pk).exists()

            if is_acceptable_user:
                return file_response(request, author_work)

        else:
            return file_response(request, author_work)

class AuthorWorkCreateView(CreateView):
    model = models.AuthorWork
    form_class = forms.AuthorWorkForm
    template_name = "create_author_work.html"
    success_url = reverse_lazy('author-categories')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs['user'] = self.request.user
        return kwargs




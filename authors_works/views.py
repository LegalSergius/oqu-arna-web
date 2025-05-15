import os
from traceback import print_tb

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.context_processors import messages
from django.http import FileResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

from django.views import View
from django.views.generic import ListView, DetailView, CreateView

from common.views import SearchView, CategoriesView

from django.contrib import messages

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





class TestView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'category.html')

class CategoriesAuthorWorksView(LoginRequiredMixin, CategoriesView):
    template_name = 'category.html'

class AuthorWorksListView(LoginRequiredMixin, SearchView):
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

class AuthorWorkDetailView(LoginRequiredMixin, DetailView):
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

class DownloadAuthorWorkView(LoginRequiredMixin, View):
    def get(self, request, author_work_id):
        author_work = models.AuthorWork.objects.get(pk=author_work_id)

        if author_work.status == Status.private:
            is_acceptable_user = author_work.acceptable_users.filter(pk=request.user.pk).exists()

            if is_acceptable_user:
                return file_response(request, author_work)

        else:
            return file_response(request, author_work)

class AuthorWorkCreateView(LoginRequiredMixin, CreateView):
    model = models.AuthorWork
    form_class = forms.AuthorWorkForm
    template_name = "create_author_work.html"
    success_url = reverse_lazy('author-categories')

    def get_initial(self):
        initial = super().get_initial()
        initial.update({"status": Status.public, "price": 0})
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs['user'] = self.request.user
        return kwargs

    def form_invalid(self, form):

        name = form.data.get("name", "")
        status = form.data.get("status", "")
        price = float(form.data.get("price", ""))


        if name == "":
            messages.error(self.request, "Пожалуйста! Введите имя работы!")

        if status == Status.private and price == 0:
            messages.error(self.request, "Пожалуйста! Укажите цену!")

        if status == "":
            messages.error(self.request, "Пожалуйста! Выберите статус!")

        return super().form_invalid(form)




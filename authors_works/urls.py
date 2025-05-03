from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('test', views.TestView.as_view(), name='test'),

    path('author_works', views.CategoriesListView.as_view(), name='author-categories'),
    path('author_works/<int:category>', views.AuthorWorksListView.as_view(), name='author-works'),
]
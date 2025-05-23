from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
<<<<<<< Updated upstream
    path('test', views.TestView.as_view(), name='test'),

    path('author_works', views.CategoriesAuthorWorksView.as_view(), name='author-categories'),
    path('author_works/<int:category>', views.AuthorWorksListView.as_view(), name='author-works'),
    path('author_work/<int:pk>', views.AuthorWorkDetailView.as_view(), name='author-work-detail'),
    path('download_author_work/<int:author_work_id>', views.DownloadAuthorWorkView.as_view(), name='author-work-download'),
    path('create_author_work', views.AuthorWorkCreateView.as_view(), name='author-work-create'),
=======
    path('test/', views.TestView.as_view(), name='test'),
    path('author_works/<int:category>', views.AuthorWorksListView.as_view(), name='author-works'),
    path('author_work/<int:pk>', views.AuthorWorkDetailView.as_view(), name='author-work-detail'),
    path('author_works/', views.CategoryListView.as_view(), name='author-categories'),
>>>>>>> Stashed changes
]
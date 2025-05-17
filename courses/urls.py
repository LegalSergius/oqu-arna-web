"""
URL configuration for oquArnaWeb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from common import views as common_views
from courses import views


lesson_creation_urlpatterns = [
    path('', views.LessonCreateView.as_view(), name='create-lesson'),
    path('content/', common_views.LessonContentView.as_view(), name='content'),
]

urlpatterns = [
    path('', views.CoursesCategoriesView.as_view(), name='courses-categories'),
    path('<int:category>', views.CoursesListView.as_view(), name='courses'),
    path('<int:course_id>/details', views.CourseDetailView.as_view(), name='course-details'),
    path('create/', views.CourseCreateView.as_view(), name='course-create'),
    path('download/<int:content_id>', views.DownloadCourseView.as_view(), name='download-guideline'),
    path('<int:course_id>/lessons', views.LessonsListView.as_view(), name='lessons'),
    path('<int:course_id>/createLesson/', include(lesson_creation_urlpatterns)),
    path('lessonStats/', TemplateView.as_view(template_name='courses/lessonStats.html'), name='lesson_stats'),
    path('schedule/', TemplateView.as_view(template_name='courses/schedule.html'), name='schedule'),
    path('', TemplateView.as_view(template_name='courses/../templates/categories/categories.html'), name='courses_categories'),
    path('entities/', TemplateView.as_view(template_name='courses/../authors_works/templates/entities.html'), name='entities')
]



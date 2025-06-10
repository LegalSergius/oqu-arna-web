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
from courses.views import LessonStatisticView

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
    path('download_task/<int:lesson_id>', views.DownloadTaskView.as_view(), name='download-task'),
    path('<int:lesson_id>/lesson_detail/', views.LessonDetailView.as_view(), name='lessons-detail'),
    path('<int:course_id>/lessons', views.LessonsListView.as_view(), name='lessons'),
    path('<int:course_id>/lessons_student', views.LessonsStudentListView.as_view(), name='lessons-student-list'),
    path('<int:course_id>/createLesson/', include(lesson_creation_urlpatterns)),
    path('<int:lesson_id>/lessons_edit/', views.LessonUpdateView.as_view(), name='lessons-update'),
    path('<int:lesson_id>/lessonStats/', LessonStatisticView.as_view(), name='lesson_stats'),
    path('schedule/', views.ScheduleView.as_view(), name='schedule'),

    path('<int:lesson_id>/redirect_test', views.get_test_lesson, name='test-redirect'),

    path('<int:test_id>/test/', views.TestView.as_view(), name='test'),
    path('<int:test_id>/test_edit/', views.TestEditView.as_view(), name='test-edit'),
    path('<int:test_id>/add_question/', views.QuestionCreateView.as_view(), name='question-create'),
    path('<int:question_id>/edit_question/', views.QuestionEditView.as_view(), name='question-edit'),
    path('<int:question_id>/remove_question/', views.RemoveQuestionView.as_view(), name='question-remove'),
    path('', TemplateView.as_view(template_name='courses/../templates/categories/categories.html'), name='courses_categories'),
    path('entities/', TemplateView.as_view(template_name='courses/../authors_works/templates/entities.html'), name='entities')
]



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

zoom_urlpatterns = [
    path('oauth/', views.zoom_oauth_start, name='zoom_oauth_start'),
    # path('oauth/callback/', views.zoom_oauth_callback, name='zoom_oauth_callback'),
    path('meeting', views.CreateZoomMeetingView.as_view(), name='meeting')
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
    path('lessonTemporarySave', views.save_lesson_temporary, name='save-lesson-temporary'),
    path('<int:course_id>/createLesson/', include(lesson_creation_urlpatterns)),
    path('zoom/', include(zoom_urlpatterns)),
    path('<int:lesson_id>/lessons_edit/', views.LessonUpdateView.as_view(), name='lessons-update'),
    path('<int:lesson_id>/lessonStats/', LessonStatisticView.as_view(), name='lesson_stats'),
    path('schedule/', views.ScheduleView.as_view(), name='schedule'),
    path('', TemplateView.as_view(template_name='courses/../templates/categories/categories.html'), name='courses_categories'),
    path('entities/', TemplateView.as_view(template_name='courses/../authors_works/templates/entities.html'), name='entities')
]


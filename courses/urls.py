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
from courses import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='courses/categories.html'), name='courses_categories'),
    path('entities/', TemplateView.as_view(template_name='courses/entities.html'), name='entities'),
    path('lessons/', TemplateView.as_view(template_name='courses/lessons.html'), name='lessons'),
    path('lessonActions/', TemplateView.as_view(template_name='courses/lessonActions.html'), name='lesson_actions'),
    path('lessonStats/', TemplateView.as_view(template_name='courses/lessonStats.html'), name='lesson_stats'),
    path('content/', TemplateView.as_view(template_name='courses/content.html'), name='content'),
    path('schedule/', TemplateView.as_view(template_name='courses/schedule.html'), name='schedule')
]

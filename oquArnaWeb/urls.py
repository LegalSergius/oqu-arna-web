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
from django.conf import settings
from django.conf.urls.static import static

from oquArnaWeb import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("staff/", views.custom_admin_home_view, name="custom_admin_home"),
    path("staff/actions/", views.actions_history_view, name="actions_history"),
    path("staff/report/", views.users_report_download, name="users_report_download"),
    path("staff/certificates/<int:course_id>/", views.download_course_certificates, name="download_course_certificates"),
    path("users/", include("users.urls")),
    path("works/", include("authors_works.urls")),

    path("", views.home_view, name="home"),

    path('accounts/', include('django.contrib.auth.urls')),# кастомная ссылка для активации
    path('courses/', include('courses.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
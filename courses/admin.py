from django.contrib import admin

from courses import models

admin.site.register(models.Course)
admin.site.register(models.Lesson)
admin.site.register(models.LessonStatistics)
admin.site.register(models.Conference)

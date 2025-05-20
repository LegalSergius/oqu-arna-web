from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from common.models import Content, Category
from datetime import timedelta

User = settings.AUTH_USER_MODEL

class Course(models.Model):
    name               = models.CharField(_('Название курса'), max_length=128)
    description        = models.TextField(_('Описание курса'))
    creator            = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentored_courses')
    start_date         = models.DateField(_('Дата начала'))
    end_date           = models.DateField(_('Дата окончания'))
    guideline          = models.ForeignKey(Content, on_delete=models.CASCADE, verbose_name=_('Методическое указание'))
    participants       = models.ManyToManyField(User, related_name='enrolled_courses', verbose_name=_('Участники'))
    participants_count = models.IntegerField(_('Кол-во участников'))
    category           = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    created_at         = models.DateTimeField(auto_now_add=True)
    updated_at         = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('курс')
        verbose_name_plural = _('курсы')

    def __str__(self):
        return self.name

class LessonStatistics(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_statistic')
    conference      = models.BooleanField(default=False)
    test            = models.BooleanField(default=False)
    task            = models.BooleanField(default=False)

    comment         = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user}"


class Lesson(models.Model):
    name            = models.CharField(_('Название занятия'), max_length=128)
    description     = models.TextField(_('Описание занятия'))
    lesson_date     = models.DateTimeField(_('Дата проведения'))
    duration        = models.DurationField(_('Продолжительность'), default=timedelta(minutes=60))
    lesson_statics  = models.ManyToManyField(LessonStatistics, related_name='lesson_statics')
    created_at      = models.DateTimeField(auto_now_add=True)
    course          = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name=_('Курс'))
    assignments     = models.ManyToManyField(Content, related_name='lessons', verbose_name=_('Материалы'), blank=True)
    class Meta:
        verbose_name = _('занятие')
        verbose_name_plural = _('занятия')

    def __str__(self):
        return f"{self.name} ({self.course.name}) - {timezone.make_naive(self.lesson_date)}"


class Conference(models.Model):
    zoom_id = models.CharField(_('Zoom ID'), max_length=64, unique=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='conferences', verbose_name=_('Занятие'))
    created_at = models.DateField(_('Дата создания'), auto_now_add=True)

    class Meta:
        verbose_name = _('конференция')
        verbose_name_plural = _('конференции')

    def __str__(self):
        return f"Conference {self.zoom_id} — {self.lesson.name}"
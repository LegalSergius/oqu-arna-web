from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.managers import CustomUserManager

app_name = 'users'
class CustomUser(AbstractUser):

    email = models.EmailField(_('E‑mail'), unique=True)

    full_name     = models.CharField(_('ФИО'), max_length=255)
    phone_number  = models.CharField(_('Телефон'), max_length=20, blank=True)
    organization  = models.CharField(_('Организация'), max_length=255, blank=True)
    country       = models.CharField(_('Страна'), max_length=100,  blank=True)
    city          = models.CharField(_('Город'),  max_length=100,  blank=True)
    is_educator   = models.BooleanField(_('Преподаватель'), default=False)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('пользователь')
        verbose_name_plural = _('пользователи')

    def __str__(self):
        return self.full_name or self.email

class Document(models.Model):
    user        = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name=_('Владелец'),
    )
    file        = models.FileField(
        upload_to='documents/',
        verbose_name=_('Файл')
    )
    title       = models.CharField(_('Название'), max_length=255)
    uploaded_at = models.DateTimeField(_('Загружено'), auto_now_add=True)

    class Meta:
        verbose_name        = _('документ')
        verbose_name_plural = _('документы')
        ordering            = ('-uploaded_at',)

    def __str__(self):
        return f'{self.title} ({self.user.email})'

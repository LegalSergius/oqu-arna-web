from django.contrib.auth import get_user_model
from django.db import models

from common.models import Content

User = get_user_model()

class Status(models.TextChoices):
    public  = 'PUBLIC', 'ОТКРЫТЫЙ'
    private = 'PRIVATE', 'ЗАКРЫТЫЙ'

class AuthorWork(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=16, choices=Status, default=Status.public)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    files = models.ManyToManyField(Content, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

from django.contrib.auth import get_user_model
from django.db import models

from common.models import Content, Category

User = get_user_model()

class Status(models.TextChoices):
<<<<<<< HEAD
    public  = 'PUBLIC', 'ОТКРЫТЫЙ'
    private = 'PRIVATE', 'ЗАКРЫТЫЙ'

class AuthorWork(models.Model):
    name                = models.CharField(max_length=100)
    status              = models.CharField(max_length=16, choices=Status, default=Status.public)
    creator             = models.ForeignKey(User, related_name='creator', on_delete=models.CASCADE, blank=False, null=False, default=1)
    category            = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, null=False, default=1)
    description         = models.TextField(blank=True, null=False, default="")
    file                = models.ForeignKey(Content, on_delete=models.CASCADE, blank=False, null=False, default=1)
    acceptable_users    = models.ManyToManyField(User, related_name='acceptable_authors', blank=True)
    price               = models.IntegerField(blank=False, null=False, default=0)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
=======
    PUBLIC  = 'PUBLIC', 'ОТКРЫТЫЙ'
    PRIVATE = 'PRIVATE', 'ЗАКРЫТЫЙ'

class AuthorWork(models.Model):
    name             = models.CharField(max_length=100)
    status           = models.CharField(
        max_length=16,
        choices=Status.choices,          # <- вот это главное
        default=Status.PUBLIC,           # хранится 'PUBLIC'
    )
    creator          = models.ForeignKey(
        User,
        related_name='created_works',    # не делай related_name='creator', это ад для реверса
        on_delete=models.CASCADE,
    )
    category         = models.ForeignKey(Category, on_delete=models.CASCADE)
    description      = models.TextField(blank=True, default="")
    file             = models.ForeignKey(Content, on_delete=models.CASCADE)
    acceptable_users = models.ManyToManyField(User, related_name='acceptable_authors', blank=True)
    price            = models.IntegerField(default=0)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
>>>>>>> origin/dima-prez

from django.contrib.auth import get_user_model
from django.db import models

<<<<<<< Updated upstream
from common.models import Content, Category
=======
import common.models
>>>>>>> Stashed changes

User = get_user_model()

class Status(models.TextChoices):
<<<<<<< Updated upstream
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
    PUBLIC  = "PUBLIC", "ОТКРЫТЫЙ"
    PRIVATE = "PRIVATE", "ЗАКРЫТЫЙ"

class AuthorWorks(models.Model):
    name        = models.CharField(max_length=128, blank=False, null=False)
    file        = models.ForeignKey(common.models.Content, on_delete=models.CASCADE, null=False, blank=False)
    category    = models.ForeignKey(common.models.Category, on_delete=models.CASCADE, null=False, blank=False)
    status      = models.CharField(max_length=10, choices=Status, default=Status.PUBLIC)
    creator     = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    edited_at   = models.DateTimeField(auto_now=True)
>>>>>>> Stashed changes

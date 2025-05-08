from django.db import models

class Content(models.Model):
    file        = models.FileField(max_length=512, blank=False, null=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)


class Category(models.Model):
    name        = models.CharField(max_length=100)
    image       = models.ForeignKey(Content, on_delete=models.CASCADE, blank=False, null=False)
    created_at  = models.DateTimeField(auto_now_add=True)

from django.db import models

class Content(models.Model):
<<<<<<< Updated upstream
    file_name   = models.CharField(max_length=250, default='')
    file        = models.FileField(max_length=512, blank=False, null=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file_name


class Category(models.Model):
    name        = models.CharField(max_length=100)
    image       = models.ForeignKey(Content, on_delete=models.CASCADE, blank=False, null=False)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
=======
    file        = models.FileField(blank=False, null=False)
    created_at  = models.DateTimeField(auto_now_add=True)

class Category(models.Model):
    name        = models.CharField(max_length=128, unique=True, blank=False, null=False)
    image       = models.ForeignKey(Content, on_delete=models.CASCADE, null=False, blank=False)
    created_at  = models.DateTimeField(auto_now_add=True)
>>>>>>> Stashed changes

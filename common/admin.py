from django.contrib import admin

<<<<<<< Updated upstream
from common import models

admin.site.register(models.Content)
=======
from . import models

admin.site.register(models.Content)

>>>>>>> Stashed changes
admin.site.register(models.Category)

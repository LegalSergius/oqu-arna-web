from django.contrib import admin

<<<<<<< Updated upstream
from authors_works import models


admin.site.register(models.AuthorWork)
=======
from . import models

admin.site.register(models.AuthorWorks)
>>>>>>> Stashed changes

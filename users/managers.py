from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
<<<<<<< Updated upstream
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
=======
    def create_user(self, email, password=None, **extra_fields):
>>>>>>> Stashed changes
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

<<<<<<< Updated upstream
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if not extra_fields['is_staff'] or not extra_fields['is_superuser']:
            raise ValueError('Для суперюзера is_staff и is_superuser должны быть True')
        return self._create_user(email, password, **extra_fields)
=======
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser должен иметь is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser должен иметь is_superuser=True.')
        return self.create_user(email, password, **extra_fields)
>>>>>>> Stashed changes

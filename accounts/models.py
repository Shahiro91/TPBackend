from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('El correo electrónico debe ser proporcionado.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    ADMIN = 'ADMIN'
    PROFESOR = 'PROFESOR'
    ALUMNO = 'ALUMNO'

    ROLE_CHOICES = [
        (ADMIN, 'Administrador'),
        (PROFESOR, 'Profesor'),
        (ALUMNO, 'Alumno'),
    ]

    username = None
    email = models.EmailField('Correo electrónico', unique=True)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ALUMNO,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

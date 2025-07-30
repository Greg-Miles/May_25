from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField('email address', unique=True, max_length=254,)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # username обязателен для создания суперпользователя

    def __str__(self):
        return self.email

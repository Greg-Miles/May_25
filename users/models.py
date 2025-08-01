from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=254,)
    username = models.CharField(max_length=150, unique=True, verbose_name="Имя пользователя")
    first_name = models.CharField(max_length=30, blank=True,
                                  verbose_name = "Имя")
    last_name = models.CharField(max_length=30, blank=True,
                                  verbose_name = "Фамилия")
    avatar = models.ImageField(upload_to='media/avatars/', blank=True, null=True,
                               verbose_name='Аватар')
    birth_date = models.DateField(blank=True, null=True, verbose_name='День рождения',)
    is_master = models.BooleanField(default=False, verbose_name='Мастер')
    telegaram = models.CharField(max_length=100, blank=True, null=True, verbose_name='Контакт в Telegram')
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='Номер телефона')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # username обязателен для создания суперпользователя

    def __str__(self):
        return self.email

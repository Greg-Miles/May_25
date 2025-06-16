from django.db import models

# Create your models here.

class Order(models.Model):
    """
    Модель записи в барбершоп.
    """
    STATUS_CHOICES = [
        ("not_approved", "Не подтверждена"),
        ("approved", "Подтверждена"),
        ("in_progress", "В процессе"),
        ("done", "Выполнена"),
    ]
    client_name = models.CharField(max_length=100, verbose_name="Имя клиента")
    phone = models.CharField(max_length=20, verbose_name="Номер телефона")
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)
    status = models.CharField(max_length=50, verbose_name="Статус заявки", choices=STATUS_CHOICES, default="not_approved")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    master = models.ForeignKey("Master", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Мастер")
    services = models.ManyToManyField("Service", verbose_name="Услуги", related_name="orders")
    appointment_date = models.DateTimeField(verbose_name="Дата и время записи")

    def __str__(self):
        return  f"{self.client_name} - {self.appointment_date}"
    
class Master(models.Model):
    """
    Модель мастера барбершопа.
    """
    name = models.CharField(max_length=100, verbose_name="Имя мастера")
    photo = models.ImageField(upload_to="masters/", verbose_name="Фото мастера", blank=True)
    phone = models.CharField(max_length=20, verbose_name="Номер телефона")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    experience = models.PositiveIntegerField(verbose_name="Стаж работы", help_text="Опыт работы в годах")
    services = models.ManyToManyField("Service", verbose_name="Услуги", related_name="masters")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    def __str__(self):
        return f"Мастер {self.name}"
    
class Review(models.Model):
    """
    Модель отыва на мастера.
    """
    RATING_CHOICES = [
        (1, "Ужасно"),
        (2, "Плохо"),
        (3, "Нормально"),
        (4, "Хорошо"),
        (5, "Отлично"),
    ]

    text = models.TextField(verbose_name="Текст отзыва")
    client_name = models.CharField(max_length=100, blank=True, default="Гость", verbose_name="Имя клиента")
    master = models.ForeignKey("Master", on_delete=models.SET_NULL, null=True, verbose_name="Мастер")
    photo = models.ImageField(upload_to="reviews/", blank=True, null=True, verbose_name="Фотография")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    rating = models.PositiveSmallIntegerField(verbose_name="Оценка", choices=RATING_CHOICES, default=5)
    is_published = models.BooleanField(default=False, verbose_name="Опубликован")

    def __str__(self):
        return f"Отзыв от {self.client_name} на {self.master.name}"


class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    duration = models.PositiveIntegerField(verbose_name="Длительность", help_text="Время выполнения в минутах", default=20)
    is_popular = models.BooleanField(default=False, verbose_name="Популярная услуга")

    def __str__(self):
        return f"Услуга: {self.name}"

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Review
from .mistral import is_good_review


@receiver(post_save, sender=Review)
def check_review(sender, instance, created, **kwargs):
    """
    Проверяет отзыв на соответствие критериям качества.
    Если отзыв не прошел проверку, то он помечается как не проверенный ИИ.
    :paaram sender: Модель, отправляющая сигнал.
    :param instance: Экземпляр модели, который был сохранен.
    :param created: Флаг, указывающий, был ли объект создан или обновлен.
    :param kwargs: Дополнительные аргументы.
    """
    if created:
        instance.ai_checked_status = "ai_checked_in_progress"
        instance.save()
        if not is_good_review(instance.text):
            instance.ai_checked_status = "ai_cancelled"
            instance.save()
        else:
            instance.ai_checked_status = "ai_checked_true"
            # Если отзыв прошел проверку, то он публикуется
            instance.is_published = True
            instance.save()
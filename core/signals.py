from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from .models import Review, Order, Service
from .mistral import is_good_review
from .telegram_bot import send_telegram_message
from barbershop.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
import asyncio


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

@receiver(m2m_changed, sender=Order.services.through)
def make_telegram_notification(sender, instance, action, **kwargs):
    """
    Отправляет уведомление в Telegram о новом заказе.
    :param sender: Модель, отправляющая сигнал.
    :param instance: Экземпляр модели, который был сохранен.
    :param action: Действие, вызвавшее сигнал.
    :param kwargs: Дополнительные аргументы.
    """
    if action == 'post_add' and kwargs.get('pk_set') and timezone.now() - instance.date_created < timedelta(seconds=5):
        # Получаем список услуг
        services = [service.name for service in instance.services.all()]

        # Формируем сообщение в MD разметке


        message = (
            f"**Новый заказ {instance.date_created.strftime('%d.%m.%Y %H:%M')}**\n"
            f"Имя: {instance.client_name}\n"
            f"Телефон: {instance.phone}\n"
            f"Мастер: {instance.master.name}\n"
            f"Услуги: {', '.join(services) or 'Не указано'}\n"
            "---\n"
            f"Комментарий: {instance.comment or 'Не указан'}\n"
            f"#заказ #{instance.master.tag_name}"
        )
        # Отправляем сообщение в телеграм
        asyncio.run(send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message))
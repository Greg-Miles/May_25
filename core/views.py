from django.shortcuts import render
from django.http import HttpResponseNotFound
from core.models import *
from django.contrib.auth.models import User

# Create your views here.

def landing(request):
    """
    Представление для главной страницы.
    :param request: запрос
    :returns render: Рендер главной страницы
    """
    context = {
        'masters': Master.objects.all(),
        'services': Service.objects.all(),
        "title": 'Барбершоп "Горшок"',
        "user" : User,
    }
    return render(request, "landing.html", context)

def thanks(request):
    """
    Представление, вызываемое при нажатии на кнопку 'Записаться'.
    :param request: запрос
    :returns render: Рендер станицы с ответом
    """
    context = {
    'masters': Master.objects.all(),
    'services': Service.objects.all(),
    "user" : User,
    }
    return render(request, 'thanks.html', context)

def orders_list(request):
    """
    Представление для просмотра всех записей.
    :param request: запрос
    :returns render: Рендер главной страницы, модифицированный для показа всех записей.
    """
    context = {
        "orders" : Order.objects.all(),
        "masters" : Master.objects.all(),
        "user" : User,
    }
    return render(request, "orders.html", context)

def order_detail(request, order_id: int):
    """
    Представление для одной записи.
    :param request: запрос
    :param order_id: номер записи в базе данных
    :returns render: Рендер главной страницы, модифицированный для показа данных о конкретной записи
    """
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return HttpResponseNotFound("Заказ не найден")
    master_name = "Мастер не назначен"
    if order.master:
        master_name = order.master.name
    context = {
        "order": Order.objects.get(id=order_id),
        "master_name": master_name,
        "user" : User,
    }
    return render(request, 'orders_detail.html', context)

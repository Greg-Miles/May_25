from django.shortcuts import render
from django.http import HttpResponseNotFound
from core.data import *
from django.contrib.auth.models import User

# Create your views here.

def landing(request):
    """
    Представление для главной страницы.
    :param request: запрос
    :returns render: Рендер главной страницы
    """
    context = {
        'masters': masters,
        'services': services,
        "title": title,
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
    'masters': masters,
    'services': services,
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
        "orders" : orders,
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
    order = [order for order in orders if order['id']== order_id][0]
    if not order:
        return HttpResponseNotFound("Заказ не найден")
    master_name = "Мастер не назначен"
    for master in masters:
        if master["id"] == order["master_id"]:
            master_name = master["name"]
            break
    context = {
        "order": order,
        "master_name": master_name,
        "user" : User,
    }
    return render(request, 'orders_detail.html', context)

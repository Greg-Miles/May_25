from django.shortcuts import render
from core.data import *

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
    }
    return render(request, 'thanks.html', context)

def orders_list(request):
    """
    Представление для просмотра всех записей.
    :param request: запрос
    :returns render: Рендер главной страницы, модифицированный для показа всех записей.
    """
    context = {
        "orders" : orders
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
    context = {
        "order": order
    }
    return render(request, 'orders_detail.html', context)

def masters_list(request):
    """
    Представление для списка всех мастеров.
    :param request: запрос
    :returns render: Рендер главной страницы, модифицированный для показа списка всех мастеров с их фото.
    """
    context = {
        "masters": masters
    }
    return render(request, 'masters_list.html', context)
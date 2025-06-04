from django.shortcuts import render
from django.http import HttpResponseNotFound
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
        "title": title
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

def services_list(request):
    """
    Представление для просмотра всех услуг барбершопа.
    :param request: запрос
    :returns render: Рендер страницы со списком всех услуг.
    """
    context = {
        "services": services,
        "title": "Наши услуги"
    }
    return render(request, "services_list.html", context)

def contacts(request):
    """
    Представление для страницы с контактами.
    :param request: запрос
    :returns render: Рендер страницы с контактами.
    """
    return render(request, "contacts.html")
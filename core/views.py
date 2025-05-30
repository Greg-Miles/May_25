from django.shortcuts import render
from core.data import *

# Create your views here.

def landing(request):
    context = {
        'masters': masters,
        'services': services,
    }
    return render(request, "landing.html", context)

def thanks(request):
    context = {
    'masters': masters,
    'services': services,
    }
    return render(request, 'thanks.html', context)

def orders_list(request):
    context = {
        "orders" : orders
    }
    return render(request, "orders.html", context)

def order_detail(request, order_id):
    order = [order for order in orders if order['id']== order_id][0]
    context = {
        "order": order
    }
    return render(request, 'orders_detail.html', context)

def masters_list(request):
    context = {
        "masters": masters
    }
    return render(request, 'masters_list.html', context)
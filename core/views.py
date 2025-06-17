from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserRegistrationForm, LoginForm
from core.models import *
from django.contrib.auth.models import User

def is_staff(user):
    """
    Проверяет, является ли пользователь мастером.
    :param user: пользователь
    :returns bool: True, если пользователь мастер, иначе False
    """
    return user.is_authenticated and user.is_staff

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

    }
    return render(request, 'thanks.html', context)


@login_required
@user_passes_test(is_staff)
def orders_list(request):
    """
    Представление для просмотра всех записей.
    :param request: запрос
    :returns render: Рендер главной страницы, модифицированный для показа всех записей.
    """
    context = {
        "orders" : Order.objects.all(),
        "masters" : Master.objects.all(),

    }
    return render(request, "orders.html", context)


@login_required
@user_passes_test(is_staff)
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

    }
    return render(request, 'orders_detail.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('landing')  # Замените на ваш URL главной страницы
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    """
    Представление для входа пользователя.
    """
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Перенаправляем на страницу, с которой пришел пользователь, или на главную
                next_page = request.POST.get('next', 'landing')
                return redirect(next_page)
        else:
            # Если форма невалидна, добавляем сообщение об ошибке
            messages.error(request, 'Неверное имя пользователя или пароль.')
            # Если запрос был отправлен из меню, перенаправляем на главную
            if request.META.get('HTTP_REFERER') and 'login' not in request.META.get('HTTP_REFERER'):
                return redirect(request.META.get('HTTP_REFERER'))
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def profile(request):
    # Проверяем, является ли пользователь мастером
    is_master = hasattr(request.user, 'master_profile')
    
    context = {
        'is_master': is_master,
    }
    
    if is_master:
        context['master'] = request.user.master_profile
    
    return render(request, 'profile.html', context)

def user_logout(request):
    """
    Представление для выхода пользователя с немедленным перенаправлением на главную страницу.
    """
    logout(request)
    return redirect('landing')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegistrationForm
from core.models import Order, Review

def register(request):
    """
    Представление для регистрации пользователя.
    :param request: запрос
    :returns render: Рендер страницы регистрации
    """

    if request.user.is_authenticated:
        return redirect('landing') # если пользователь уже авторизован, перенаправляем на главную страницу
      
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('landing') # если регистрация прошла успешно, также перенаправляем на главную страницу
        else:
            messages.error(request, 'Ошибка регистрации. Пожалуйста, проверьте введенные данные.')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    """
    Представление для входа пользователя.
    :param request: запрос
    :returns render: Рендер страницы входа
    """
    if request.user.is_authenticated:
        return redirect('landing')  # если пользователь уже авторизован, перенаправляем на главную страницу

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
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
            if'login' not in request.path:
                referer = request.META.get('HTTP_REFERER', 'landing')
                return redirect(referer)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    """
    Представление для выхода пользователя с немедленным перенаправлением на главную страницу.
    :param request: запрос
    :returns redirect: Перенаправление на главную страницу
    """
    logout(request)
    return redirect('landing')

@login_required
def profile(request):
    """
    Представление для профиля пользователя.
    :param request: запрос
    :returns render: Рендер страницы профиля
    """
    # Проверяем, является ли пользователь мастером
    is_master = hasattr(request.user, 'master_profile')
    
    context = {
        'user': request.user,
        'is_master': is_master,
    }
    
    if is_master:
        master = request.user.master_profile
        context['master'] = master
        orders = Order.objects.filter(master=master).order_by('-appointment_date')
        context['orders'] = orders

        reviews = Review.objects.filter(master=master, is_published=True).order_by('-created_at')
        context['reviews'] = reviews
    else:
        # Если пользователь не мастер, получаем его заказы
        orders = Order.objects.filter(client_name=request.user.username).order_by('-appointment_date')
        context['orders'] = orders
    
    return render(request, 'profile.html', context)


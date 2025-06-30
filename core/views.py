from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from .forms import UserRegistrationForm, OrderForm, ReviewForm
from core.models import *
from django.contrib.auth.models import User


def is_staff(user):
    """
    Проверяет, является ли пользователь мастером.
    :param user: пользователь
    :returns bool: True, если пользователь мастер, иначе False
    """
    return user.is_staff

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
        'reviews': Review.objects.filter(is_published=True).order_by('-created_at')[:5],
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
    q = request.GET.get("q")
    search_by_phone = request.GET.get("search_by_phone", "false") == "true"
    search_by_name  = request.GET.get("search_by_name", "false") == "true"
    search_by_comment = request.GET.get("search_by_comment", "false") == "true"

    order_by_date = request.GET.get("order_by_date", "desc")

    status_not_approved = request.GET.get("status_not_approved", "false") == "true"
    status_approved = request.GET.get("status_approved", "false") == "true"
    status_in_progress = request.GET.get("status_in_progress", "false") == "true"
    status_done = request.GET.get("status_done", "false") == "true"
    status_canceled = request.GET.get("status_canceled", "false") == "true"

    query = Order.objects.all()

    base_q = Q()

    if q:
        if search_by_phone:
            base_q |= Q(phone__icontains=q)
        if search_by_name:
            base_q |= Q(master__name__icontains=q)
        if search_by_comment:
            base_q |= Q(comment__icontains=q)

    if order_by_date == "asc":
        query = query.order_by("date_created")
    else:
        query = query.order_by("-date_created")

    if status_not_approved:
        base_q |= Q(status="not_approved")
    if status_approved:
        base_q |= Q(status="approved")
    if status_in_progress:
        base_q |= Q(status="in_progress")
    if status_done:
        base_q |= Q(status="done")
    if status_canceled:
        base_q |= Q(status="canceled")
    orders = query.filter(base_q)
    context = {
        "orders" : orders,
        "title": 'Список заказов',
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
    """
    Представление для регистрации пользователя.
    :param request: запрос
    :returns render: Рендер страницы регистрации
    """
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
    :param request: запрос
    :returns render: Рендер страницы входа
    """
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

def user_logout(request):
    """
    Представление для выхода пользователя с немедленным перенаправлением на главную страницу.
    :param request: запрос
    :returns redirect: Перенаправление на главную страницу
    """
    logout(request)
    return redirect('landing')


def get_master_services(request):
    """
    AJAX представление для получения услуг мастера.
    """
    master_id = request.GET.get('master_id')
    if master_id:
        try:
            master = Master.objects.get(id=master_id)
            services = master.services.all()
            services_data = [{'id': service.id, 'name': service.name, 'price': service.price} for service in services]
            return JsonResponse({'services': services_data})
        except Master.DoesNotExist:
            return JsonResponse({'services': []})
    return JsonResponse({'services': []})

def make_order(request, master_id=None):
    """
    Представление для создания заказа.
    :param request: запрос
    :param master_id: идентификатор мастера (по умолчанию None)
    :returns render: Рендер страницы создания заказа
    """
    if request.method == 'POST':
        form = OrderForm(request.POST, master_id=master_id)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.client_name = request.user.username
            order.save()
            form.save_m2m()
            return redirect('thanks')
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data['client_name'] = request.user.username

        if master_id:
            try:
                master = Master.objects.get(id=master_id)
                initial_data['master'] = master
            except Master.DoesNotExist:
                pass
        form = OrderForm(initial=initial_data, master_id=master_id)
    
    masters = Master.objects.all()
    selected_master_id = int(master_id) if master_id else None
    context = {
        'form': form, 
        'masters': masters,
        'selected_master_id': selected_master_id,
        }
    return render(request, 'make_order.html', context)


def master_detail(request, master_id):
    """
    Представление для просмотра деталей мастера и добавления отзывов.
    :param request: запрос
    :param master_id: идентификатор мастера
    :returns render: Рендер страницы деталей мастера
    """
    master = get_object_or_404(Master, id=master_id)
    services = Service.objects.filter(masters=master)
    
    # Get published reviews for this master
    reviews = Review.objects.filter(master=master, is_published=True,).order_by('-created_at')[:5]
    
    # Handle review submission
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.master = master
            
            # Set the client name based on authentication status
            if request.user.is_authenticated:
                review.client_name = request.user.username
            else:
                review.client_name = "Гость"
                
            # Set review as unpublished until approved (optional)
            review.is_published = False
            
            review.save()
            messages.success(request, 'Спасибо за ваш отзыв! Он будет опубликован после проверки.')
            return redirect('master_detail', master_id=master_id)
    else:
        form = ReviewForm()
    
    context = {
        'master': master,
        'services': services,
        'reviews': reviews,
        'form': form,
    }
    
    return render(request, 'master_detail.html', context)


def make_review(request):
    """
    Представление для создания отзыва.
    :param request: запрос
    :returns render: Рендер страницы создания отзыва
    """
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.is_published = False  # Set the review as unpublished until approved
            review.save()
            messages.success(request, 'Спасибо за ваш отзыв! Он будет опубликован после проверки.')
            return redirect('master_detail', master_id=review.master.id)
    else:
        form = ReviewForm()

        initial_data = {}
        if request.user.is_authenticated:
            initial_data['client_name'] = request.user.username
        else:
            initial_data['client_name'] = "Гость"
        form = ReviewForm(initial=initial_data)

    context = {
        'form': form,
    }

    return render(request, 'make_review.html', context)
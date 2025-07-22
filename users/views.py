from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegistrationForm
from core.models import Order, Review
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


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



class ProfileView(LoginRequiredMixin, TemplateView):
    """
    Класс представления для профиля пользователя.
    """
    template_name = 'profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Проверяем, является ли пользователь мастером
        is_master = hasattr(user, 'master_profile')
        
        context.update({
            'user': user,
            'is_master': is_master,
        })
        
        if is_master:
            master = user.master_profile
            context['master'] = master
            orders = Order.objects.filter(master=master).order_by('-appointment_date')
            context['orders'] = orders

            reviews = Review.objects.filter(master=master, is_published=True).order_by('-created_at')
            context['reviews'] = reviews
        else:
            # Если пользователь не мастер, получаем его заказы
            orders = Order.objects.filter(client_name=user.username).order_by('-appointment_date')
            context['orders'] = orders
        
        return context


class UserCancelOrderView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Представление для отмены заказа клиентом.
    """
    model = Order
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        order_id = self.kwargs.get('pk')
        return get_object_or_404(Order, id=order_id, client_name=self.request.user.username)
    
    def test_func(self):
        """
        Проверяем, что пользователь может отменить этот заказ.
        """
        order = self.get_object()
        # Проверяем, что заказ принадлежит пользователю и его можно отменить
        return (order.client_name == self.request.user.username and 
                order.status not in ['done', 'canceled'])



    def delete(self, request, *args, **kwargs):
        order = self.get_object()
        order.status = 'canceled'
        order.save()
        messages.success(request, f'Заказ #{order.id} успешно отменен!')
        return redirect(self.success_url)


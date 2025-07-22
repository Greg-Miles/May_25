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


class RegistrationView(CreateView):
    """
    Класс представления для регистрации пользователя.
    """
    model = User
    form_class = UserRegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('landing')

    def form_valid(self, form):
        """
        Обработка валидной формы.
        """
        user = form.save()
        login(self.request, user)
        return redirect('landing')



class UserLoginView(UserPassesTestMixin,TemplateView):
    """
    Класс представления для страницы входа пользователя.
    """
    template_name = 'login.html'

    def test_func(self):
        """
        Проверка, обратная LoginRequiredMixin.
        """
        return not self.request.user.is_authenticated
    
    def handle_no_permission(self):
        """
        Переопределяем обработку отсутствия разрешения.
        """
        messages.error(self.request, "Сначала надо выйти из аккаунта")
        return redirect('landing')
    
    def get(self, request, *args, **kwargs):

        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
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
        return render(request, self.template_name, {'form': form})
    

class UserLogoutView(LoginRequiredMixin, TemplateView):
    """
    Класс представления для выхода пользователя с немедленным перенаправлением на главную страницу.
    """
    
    def get(self, request, *args, **kwargs):
        """
        Обработка GET-запроса.
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
            orders = Order.objects.filter(client_name=user.username).exclude(status='canceled').order_by('-appointment_date')
            context['orders'] = orders
        
        return context


class UserCancelOrderView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Представление для отмены заказа клиентом.
    """
    model = Order
    fields = []
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        """
        Получаем объект заказа, который пользователь хочет отменить.
        """
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

    def form_valid(self, form):
        """
        Обновляем статус заказа на 'canceled'
        """
        order = self.get_object()
        order.status = 'canceled'
        order.save()
        messages.success(self.request, 'Заказ успешно отменен!')
        return redirect(self.success_url)
    

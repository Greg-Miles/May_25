from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from .forms import OrderForm, ReviewForm
from core.models import *
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy



def is_staff(user):
    """
    Проверяет, является ли пользователь мастером.
    :param user: пользователь
    :returns bool: True, если пользователь мастер, иначе False
    """
    return user.is_staff

class LandingView(TemplateView):
    """
    Класс представления для главной страницы.
    """
    template_name = 'landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['masters'] = Master.objects.all()
        context['services'] = Service.objects.all()
        context['reviews'] = Review.objects.filter(is_published=True).order_by('-created_at')[:5]
        context["title"] = 'Барбершоп "Горшок"'
        return context


class ThanksView(TemplateView):
    """
    Класс представления для страницы с ответом после успешной записи.
    """
    template_name = 'thanks.html'


class OrderListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    Класс представления для просмотра всех записей.
    """
    model = Order
    template_name = 'orders.html'
    context_object_name = 'orders'
    ordering = ['-date_created']

    def test_func(self):
        """
        Проверка, является ли пользователь мастером.
        """
        return self.request.user.is_staff
    
    def get_queryset(self):
        """
        Обработка фильтров и сортировки поиска.
        """
        q = self.request.GET.get("q")
        search_by_phone = self.request.GET.get("search_by_phone", "false") == "true"
        search_by_name  = self.request.GET.get("search_by_name", "false") == "true"
        search_by_comment = self.request.GET.get("search_by_comment", "false") == "true"

        order_by_date = self.request.GET.get("order_by_date", "desc")

        status_not_approved = self.request.GET.get("status_not_approved", "false") == "true"
        status_approved = self.request.GET.get("status_approved", "false") == "true"
        status_in_progress = self.request.GET.get("status_in_progress", "false") == "true"
        status_done = self.request.GET.get("status_done", "false") == "true"
        status_canceled = self.request.GET.get("status_canceled", "false") == "true"

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
        return orders



class OrderDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    Класс представления для одной записи.
    """
    model = Order
    template_name = 'orders_detail.html'
    context_object_name = 'order'

    def test_func(self):
        """
        Проверка, является ли пользователь мастером.
        """
        return self.request.user.is_staff


# Представление для отмены заказа клиентом (опционально)
@login_required
def cancel_my_order(request, order_id):
    """
    Представление для отмены своего заказа клиентом.
    """
    order = get_object_or_404(Order, id=order_id, client_name=request.user.username)
    
    # Проверяем, можно ли отменить заказ (например, только если он еще не в работе)
    if order.status in ['done', 'canceled']:
        messages.error(request, 'Этот заказ нельзя отменить.')
        return redirect('my_order_detail', order_id=order.id)
    
    if request.method == 'POST':
        order.status = 'canceled'
        order.save()
        messages.success(request, f'Заказ #{order.id} успешно отменен!')
        return redirect('my_orders')
    
    context = {
        'order': order,
        'title': f'Отмена заказа #{order.id}'
    }
    return render(request, 'orders/cancel.html', context)



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
    else:
        services = Service.objects.all()
        services_data = [{'id': service.id, 'name': service.name, 'price': service.price} for service in services]
    return JsonResponse({'services': services_data})


class OrderCreateView(CreateView):
    """
    Класс представления для создания заказа.
    """
    model = Order
    form_class = OrderForm
    template_name = 'make_order.html'
    success_url = reverse_lazy('thanks')

    def get_context_data(self, **kwargs):
        """
        Получает контекст данных для рендеринга шаблона.
        """
        context = super().get_context_data(**kwargs)
        context['masters'] = Master.objects.all()
        context['selected_master_id'] = self.kwargs.get('pk')
        context['action'] = "create"
        context['title'] = 'Записаться на услугу'
        context['submit_text'] = "Записаться"
        return context
    
    def get_initial(self):
        """
        Устанавливаем начальные значения для формы.
        """
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial['client_name'] = self.request.user.username

        if 'pk' in self.kwargs:
            try:
                master = Master.objects.get(id=self.kwargs['pk'])
                initial['master'] = master
            except Master.DoesNotExist:
                pass
        return initial

    def form_valid(self, form):
        """
        Обрабатывает валидную форму.
        """
        order = form.save(commit=False)
        if self.request.user.is_authenticated:
            order.client_name = self.request.user.username
        order.save()
        messages.success(self.request, "Заказ успешно создан!")
        return super().form_valid(form)


# UPDATE - редактирование заказа (только для персонала)
@login_required
@user_passes_test(is_staff)
def update_order(request, order_id):
    """
    Представление для редактирования заказа (только для персонала).
    """
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order, is_staff=request.user.is_staff)
        if form.is_valid():
            form.save()
            messages.success(request, f'Заказ {order.id} успешно обновлен!')
            return redirect('orders_list')
        messages.error(request, "Ошибка при обновлении заказа. Пожалуйста, проверьте введенные данные.")
    else:
        form = OrderForm(instance=order, is_staff=request.user.is_staff)
    
    context = {
        'form': form, 
        'order': order,
        'title': f'Редактирование заказа #{order.id}',
        'action': 'update',
        'submit_text': 'Сохранить изменения'
    }
    return render(request, 'make_order.html', context)

# DELETE - удаление заказа (только для персонала)
@login_required
@user_passes_test(is_staff)
def delete_order(request, order_id):
    """
    Представление для удаления заказа (только для персонала).
    """
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order_id_for_message = order.id
        order.delete()
        messages.success(request, f'Заказ #{order_id_for_message} успешно удален!')
        return redirect('orders_list')
    
    context = {
        'order': order,
        'title': f'Удаление заказа #{order.id}'
    }
    return render(request, 'delete_order.html', context)


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
        form = ReviewForm(request.POST or None, 
                  initial={
                    'master': master.id,
                    'client_name': request.user.username or 'Гость'
                  })
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



class ReviewCreateView(CreateView):
    """
    Представление для создания отзыва.
    """
    model = Review
    form_class = ReviewForm
    template_name = 'make_review.html'
    success_url = reverse_lazy('thanks')

    def form_valid(self, form):
        review = form.save(commit=False)
        review.is_published = False  # Не публикуем отзыв пока яишенка не проверит.
        review.save()
        messages.success(self.request, 'Спасибо за ваш отзыв! Он будет опубликован после проверки.')
        return super().form_valid(form)
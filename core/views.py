from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound, JsonResponse, HttpResponseRedirect
from django.contrib import messages
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


# CREATE - создание заказа
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
class UpdateOrderView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Класс представления для обновления заказа.
    """
    model = Order
    form_class = OrderForm
    template_name = 'make_order.html'
    success_url = reverse_lazy('orders_list')

    def test_func(self):
        """
        Проверяет, является ли пользователь мастером.
        """
        return self.request.user.is_staff
    
    def get_context_data(self, **kwargs):
        """
        Получает контекст данных для рендеринга шаблона.
        """
        context = super().get_context_data(**kwargs)
        context['action'] = "update"
        context['title'] = f'Редактирование заказа #{self.object.id}'
        context['submit_text'] = "Сохранить изменения"
        return context
    
    def form_valid(self, form):
        """
        Обрабатывает валидную форму и сохраняет изменения.
        """
        messages.success(self.request, f'Заказ #{self.object.id} успешно обновлен!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """
        Обрабатывает невалидную форму и возвращает ошибки.
        """
        messages.error(self.request, "Ошибка при обновлении заказа. Пожалуйста, проверьте введенные данные.")
        return super().form_invalid(form)
    
    def get(self, request, *args, **kwargs):
        """
        Обрабатывает GET запрос для отображения формы редактирования заказа.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(form=form)
        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        """
        Обрабатывает POST запрос для обновления заказа.
        """
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        


# DELETE - удаление заказа (только для персонала)
class DeleteOrderView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Класс представления для удаления заказа.
    """
    model = Order
    template_name = 'delete_order.html'
    success_url = reverse_lazy('orders_list')
    def test_func(self):
        """
        Проверяет, является ли пользователь мастером.
        """
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        """
        Получает контекст данных для рендеринга шаблона.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление заказа #{self.object.id}'
        return context

    def post(self, request, *args, **kwargs):
        """
        Обрабатывает POST запрос для удаления заказа.
        """
        self.object = self.get_object()
        order_id_for_message = self.object.id
        
        # Добавляем сообщение
        messages.success(request, f'Заказ #{order_id_for_message} успешно удален!')
        
        # Удаляем объект
        self.object.delete()
        
        # Возвращаем редирект
        return HttpResponseRedirect(self.get_success_url())

    def get(self, request, *args, **kwargs):
        """
        Обрабатывает GET запрос для отображения страницы удаления заказа.
        """
        self.object = self.get_object()
        context = self.get_context_data()
        return self.render_to_response(context)


class MasterDetailView(DetailView):
    """
    Представление для просмотра деталей мастера.
    """
    model = Master
    template_name = 'master_detail.html'
    context_object_name = 'master'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        master = self.get_object()
        services = Service.objects.filter(masters=master)
        reviews = Review.objects.filter(master=master, is_published=True,).order_by('-created_at')[:5]
        form = ReviewForm()
        context['services'] = services
        context['reviews'] = reviews
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        """
        Обрабатывает POST запрос для добавления отзыва.
        """
        self.object = self.get_object()
        form = ReviewForm(request.POST or None,
                  initial={
                    'master': self.object.id,
                    'client_name': request.user.username or 'Гость'
                  })
        if form.is_valid():
            review = form.save(commit=False)
            review.master = self.object

            # Если пользователь аутентифицирован, используем его имя
            # иначе используем "Гость"
            if request.user.is_authenticated:
                review.client_name = request.user.username
            else:
                review.client_name = "Гость"

            # Ревью не публикуем пока яишенка не проверит.
            review.is_published = False

            review.save()
            messages.success(request, 'Спасибо за ваш отзыв! Он будет опубликован после проверки.')
            return redirect('master_detail', pk=self.object.id)


# CREATE - создание отзыва
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
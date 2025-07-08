from django.contrib import admin
from .models import Order, Master, Review, Service

class MasterAdmin(admin.ModelAdmin):
    """
    Настройки отображения и фильтрации модели Master в админ-панели.
    """
    list_display = ('name', 'user', 'phone', 'experience', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'phone')
    filter_horizontal = ('services',)
    list_editable = ('is_active',)
    
    # Добавляем возможность фильтровать по связанному пользователю
    raw_id_fields = ('user',)

class OrderAdmin(admin.ModelAdmin):
    """
    Настройки отображения и фильтрации модели Order в админ-панели.
    """
    list_display = ('client_name', 'appointment_date', 'master', 'services_display', 'status')
    list_filter = ('status', 'master')
    search_fields = ('client_name', 'phone')
    filter_horizontal = ('services',)
    list_editable = ('status', 'master', 'appointment_date')
    actions = ['mark_as_done']

    @admin.display(description='Услуги')
    def services_display(self, obj):
        """
        Поле для отображения списка услуг в админ-панели.
        """
        return ", ".join([service.name for service in obj.services.all()])
    
    @admin.action(description='Пометить как выполненные')
    def mark_as_done(self, request, queryset):
        """
        Действие для пометки выбранных заказов как выполненных.
        """
        queryset.update(status='done')


class ReviewAdmin(admin.ModelAdmin):
    """
    Настройки отображения и фильтрации модели Review в админ-панели.
    """
    list_display = ('client_name', 'master', 'rating', 'created_at', 'is_published')
    list_filter = ('rating', 'is_published', 'master')
    search_fields = ('client_name', 'text')
    actions = ['publish',]

    @admin.action(description='Опубликовать')
    def publish(self, request, queryset):
        """
        Действие для публикации выбранных отзывов.
        """
        queryset.update(is_published=True)

    
class ServiceAdmin(admin.ModelAdmin):
    """
    Настройки отображения и фильтрации модели Service в админ-панели.
    """
    list_display = ('name', 'description', 'price', 'duration', 'is_popular')
    list_filter = ('is_popular',)
    search_fields = ('name', 'description')
    list_editable = ('is_popular',)



admin.site.register(Order, OrderAdmin)
admin.site.register(Master, MasterAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Service, ServiceAdmin)

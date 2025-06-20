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
    
    # Добавляем возможность фильтровать по связанному пользователю
    raw_id_fields = ('user',)

class OrderAdmin(admin.ModelAdmin):
    """
    Настройки отображения и фильтрации модели Order в админ-панели.
    """
    list_display = ('client_name', 'appointment_date', 'master', 'status')
    list_filter = ('status', 'master')
    search_fields = ('client_name', 'phone')
    filter_horizontal = ('services',)

class ReviewAdmin(admin.ModelAdmin):
    """
    Настройки отображения и фильтрации модели Review в админ-панели.
    """
    list_display = ('client_name', 'master', 'rating', 'created_at', 'is_published')
    list_filter = ('rating', 'is_published', 'master')
    search_fields = ('client_name', 'text')

class ServiceAdmin(admin.ModelAdmin):
    """
    Настройки отображения и фильтрации модели Service в админ-панели.
    """
    list_display = ('name', 'price', 'duration', 'is_popular')
    list_filter = ('is_popular',)
    search_fields = ('name', 'description')

admin.site.register(Order, OrderAdmin)
admin.site.register(Master, MasterAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Service, ServiceAdmin)

from django.contrib import admin
from .models import Order, Master, Review, Service

class MasterAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'is_active')
    search_fields = ('name', 'phone')
    list_filter = ('is_active',)
    
    def save_model(self, request, obj, form, change):
        # Если мастер связан с пользователем, делаем этого пользователя staff
        if obj.user and not obj.user.is_staff:
            obj.user.is_staff = True
            obj.user.save()
        super().save_model(request, obj, form, change)

# Register your models here.

admin.site.register(Order)
admin.site.register(Master)
admin.site.register(Review)
admin.site.register(Service)

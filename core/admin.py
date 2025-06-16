from django.contrib import admin
from .models import Order, Master, Review, Service

# Register your models here.

admin.site.register(Order)
admin.site.register(Master)
admin.site.register(Review)
admin.site.register(Service)
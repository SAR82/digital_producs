from django.contrib import admin

from .models import Payment, Gateways


@admin.register(Gateways)
class GatewayAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_enable']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'package', 'gateway', 'status', 'price', 'phone_number', 'created_time']
    list_filter = [ 'package', 'gateway', 'status']
    search_fields = ['user_username', 'phone_number']
from django.contrib import admin

from .models import Subscription, Package


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['title', 'sku', 'price', 'is_enable', 'duration']

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'package', 'created_time', 'expire_time']

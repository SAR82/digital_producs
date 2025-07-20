from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .models import User, Province

class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone_number', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'phone_number', 'email', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'phone_number', 'email', 'is_staff')
    search_fields = ('username', 'phone_number', 'email')
    ordering = ('-id',)
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        try:
            if search_term.isdigit():
                queryset |= self.model.objects.filter(phone_number__icontains=search_term)
        except AttributeError:
            pass
        return queryset, use_distinct
admin.site.register(User, MyUserAdmin)
admin.site.register(Province)
admin.site.unregister(Group)


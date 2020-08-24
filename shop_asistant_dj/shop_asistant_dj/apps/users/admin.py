from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('telegram_id', 'is_staff', 'is_active',)
    list_filter = ('telegram_id', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('telegram_id', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('telegram_id', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('telegram_id',)
    ordering = ('telegram_id',)


admin.site.register(CustomUser, CustomUserAdmin)

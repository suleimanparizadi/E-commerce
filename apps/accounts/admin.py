from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.accounts.models.user import User
from apps.accounts.models.OTPModel import OTP
from apps.accounts.models.pending_registration import PendingRegistration


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['phone_number', 'first_name', 'last_name', 'email', 'is_active', 'is_admin', 'created_at']
    list_filter = ['is_active', 'is_admin', 'created_at']
    search_fields = ['phone_number', 'first_name', 'last_name', 'email']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Personal Info', {'fields': ('phone_number', 'first_name', 'last_name', 'email', 'date_of_birth')}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login_at', 'created_at', 'updated_at')}),
    )
    readonly_fields = ['created_at', 'updated_at', 'last_login_at']
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'code', 'attempts', 'created_at', 'expired_at', 'is_expired']
    list_filter = ['created_at']
    search_fields = ['phone_number']
    readonly_fields = ['code', 'attempts', 'created_at', 'expired_at']


@admin.register(PendingRegistration)
class PendingRegistrationAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'first_name', 'last_name', 'email', 'created_at', 'expired_at', 'is_expired']
    list_filter = ['created_at']
    search_fields = ['phone_number', 'first_name', 'last_name', 'email']
    readonly_fields = ['created_at', 'expired_at']
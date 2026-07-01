from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import pending_registration, user, OTPModel


@admin.register(user.User)
class UserAdmin(BaseUserAdmin):
    """Custom User admin with phone number as primary identifier."""
    
    list_display = [
        'phone_number', 'first_name', 'last_name', 'email',
        'is_active', 'is_admin', 'created_at', 'last_login_at'
    ]
    list_filter = ['is_active', 'is_admin', 'created_at']
    search_fields = ['phone_number', 'first_name', 'last_name', 'email']
    ordering = ['-created_at']
    readonly_fields = ['uuid', 'created_at', 'updated_at', 'last_login_at']
    
    fieldsets = (
        (_('Login Info'), {
            'fields': ('phone_number', 'password')
        }),
        (_('Personal Info'), {
            'fields': ('first_name', 'last_name', 'email', 'date_of_birth')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_admin', 'is_superuser', 'groups', 'user_permissions')
        }),
        (_('Security'), {
            'fields': ('uuid', 'last_login_at')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )


@admin.register(OTPModel.OTP)
class OTPAdmin(admin.ModelAdmin):
    """OTP admin for monitoring verification codes."""
    
    list_display = ['phone_number', 'code', 'attempts', 'created_at', 'expired_at', 'is_expired']
    list_filter = ['created_at']
    search_fields = ['phone_number']
    readonly_fields = ['code', 'attempts', 'created_at', 'expired_at']
    ordering = ['-created_at']
    fieldsets = (
        (None, {
            'fields': ('phone_number', 'code')
        }),
        (_('Security'), {
            'fields': ('attempts', 'created_at', 'expired_at')
        }),
    )
    
    def is_expired(self, obj):
        """Show if OTP is expired in list display."""
        return obj.is_expired()
    is_expired.boolean = True
    is_expired.short_description = _('Expired')


@admin.register(pending_registration.PendingRegistration)
class PendingRegistrationAdmin(admin.ModelAdmin):
    """Monitor pending registrations before verification."""
    
    list_display = [
        'phone_number', 'first_name', 'last_name', 'email',
        'created_at', 'is_expired'
    ]
    list_filter = ['created_at']
    search_fields = ['phone_number', 'first_name', 'last_name', 'email']
    readonly_fields = ['created_at', 'password']
    ordering = ['-created_at']
    
    fieldsets = (
        (_('User Info'), {
            'fields': ('phone_number', 'first_name', 'last_name', 'email', 'date_of_birth')
        }),
        (_('Security'), {
            'fields': ('password', 'created_at')
        }),
    )
    
    def is_expired(self, obj):
        """Show if pending registration is expired."""
        from django.utils import timezone
        return obj.created_at < timezone.now() - timezone.timedelta(hours=1)
    is_expired.boolean = True
    is_expired.short_description = _('Expired')
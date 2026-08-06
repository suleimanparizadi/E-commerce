from django.contrib import admin
from apps.order.models.order_model import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['product', 'quantity', 'price_at_purchase']
    extra = 0
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_amount', 'shipping_city', 'created_at']
    list_filter = ['status', 'created_at', 'shipping_city']
    search_fields = ['id', 'user__phone_number', 'user__first_name', 'user__last_name']
    readonly_fields = ['user', 'total_amount', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    ordering = ['-created_at']
    
    fieldsets = (
        ('Order Info', {
            'fields': ('id', 'user', 'status', 'total_amount')
        }),
        ('Shipping', {
            'fields': ('shipping_city', 'shipping_address', 'shipping_postal_code')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price_at_purchase']
    search_fields = ['order__id', 'product__name']
    readonly_fields = ['order', 'product', 'quantity', 'price_at_purchase']
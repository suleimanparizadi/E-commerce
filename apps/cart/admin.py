from django.contrib import admin
from apps.cart.models.cart import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    readonly_fields = ['product', 'quantity']
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_key', 'created_at', 'updated_at']
    search_fields = ['user__phone_number', 'session_key']
    inlines = [CartItemInline]
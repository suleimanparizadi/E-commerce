
from django.contrib import admin
from django.utils.html import format_html
from apps.products.models import Category, Product, ProductImage, CPU


class ProductImageInline(admin.TabularInline):
    """Inline for product gallery images."""
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'is_active', 'created_at']
    list_filter = ['is_active', 'parent']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']


@admin.register(CPU)
class CPUAdmin(admin.ModelAdmin):
    list_display = ['manufacturer', 'series', 'model', 'cores']
    list_filter = ['manufacturer']
    search_fields = ['series', 'model']
    ordering = ['manufacturer', 'series']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'brand', 'category', 'price', 'stock',
        'is_active', 'display_thumbnail', 'created_at'
    ]
    list_filter = [
        'is_active', 'category', 'brand', 'cpu__manufacturer',
        'on_board_gpu', 'touch_screen'
    ]
    search_fields = ['name', 'brand', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'brand', 'description')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock')
        }),
        ('Specifications', {
            'fields': (
                'cpu', 'ram', 'storage', 'on_board_gpu',
                'gpu', 'touch_screen', 'display_size'
            )
        }),
        ('Media', {
            'fields': ('thumbnail',)
        }),
        ('Status & Dates', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )
    inlines = [ProductImageInline]

    def display_thumbnail(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="width: 50px; height: auto;" />',
                obj.thumbnail.url
            )
        return "-"
    display_thumbnail.short_description = 'Thumbnail'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'alt_text', 'created_at']
    search_fields = ['product__name', 'alt_text']
    list_filter = ['created_at']